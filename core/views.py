from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.db.models import Q
from .models import CustomUser, Profile
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ProfileSerializer, ProfileUpdateSerializer, ChangePasswordSerializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_telephone = serializer.validated_data['email_or_telephone']
            password = serializer.validated_data['password']

            # Try to authenticate by email first, and if that fails, try with telephone
            user = CustomUser.objects.filter(
                Q(email=email_or_telephone) | Q(telephone=email_or_telephone)
            ).first()

            if user is not None and user.check_password(password):
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Logout the user by destroying their session
        request.auth.delete()  # Delete the authentication token
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        

class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        try:
            # Try to get the user's profile
            profile = Profile.objects.get(user=user)
            return profile
        except Profile.DoesNotExist:
            # If the profile doesn't exist, create a new one
            profile = Profile(user=user)
            profile.save()
            return profile

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check if the old password is correct
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': ['Incorrect password.']}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            # Update the user's session to maintain login status
            update_session_auth_hash(request, user)
            return Response({'message': 'Password successfully changed.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    def post(self, request):
        form = PasswordResetForm(request.data)
        if form.is_valid():
            view = PasswordResetView.as_view()
            return view(request)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)