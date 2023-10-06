from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.db.models import Q
from .models import CustomUser, Profile
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ProfileSerializer, ProfileUpdateSerializer, ChangePasswordSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from kidtv.models import Video
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required 
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            response_data =   {'status': True, 'token': token.key}
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response_data = {'status': False, 'error': str(e)}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


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

        return Response({'detail': 'incorrect email/telephone or password'}, status=status.HTTP_400_BAD_REQUEST)

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
        
@login_required  # Optional: You can also require the user to be logged in
@superuser_required  # Apply the custom decorator
def dashboard(request):
    users = CustomUser.objects.all()
    videos= Video.objects.all()
    all_views=Video.objects.aggregate(Sum('view_count'))['view_count__sum'] or 0
    total_users = CustomUser.objects.count()
    total_videos = Video.objects.count()
    context = {'users': users, 'total_users': total_users, 
        "videos":videos, "total_videos":total_videos, "all_views":all_views}
    return render(request, "accounts/dashboard.html", context)

@login_required  # Optional: You can also require the user to be logged in
@superuser_required  # Apply the custom decorator
def video_list(request):
    videos=Video.objects.all()
    context={"videos":videos}
    
    return render(request, "accounts/videos_list.html",context)

@login_required  # Optional: You can also require the user to be logged in
@superuser_required  # Apply the custom decorator
def user_list(request):
    users = CustomUser.objects.all()
    context= {'users': users}
    return render(request, 'accounts/all_users.html', context)

@login_required  # Optional: You can also require the user to be logged in
@superuser_required  # Apply the custom decorator
def add_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        full_name = request.POST.get('full_name', '')
        telephone = request.POST.get('telephone', '')

        # Create a new user instance using CustomUser model and manager
        user = CustomUser.objects.create_user(email=email, password=password)
        user.full_name = full_name
        user.telephone = telephone
        if user.is_superuser:
            user.role = 'admin'
        else:
            user.role = 'Guardian'

        user.save()
        return redirect('user_list')  # Redirect to a page displaying the list of users

    return render(request, 'accounts/add_user.html')

@login_required  # Optional: You can also require the user to be logged in
@superuser_required  # Apply the custom decorator
def edit_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        # Handle the form submission and update the video object
        video.title = request.POST.get('title')
        video.description = request.POST.get('description')
        video.save()
        return redirect('video_list')

    return render(request, 'accounts/edit_video.html', {'video': video})

# Delete Video View
@login_required  # Optional: You can also require the user to be logged in
@superuser_required  # Apply the custom decorator
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        # Handle the video deletion
        video.delete()
        return redirect('video_list')

    return render(request, 'accounts/delete_video.html', {'video': video})



def adminlogin(request):
    if request.method == 'POST':
        email_or_telephone = request.POST.get('email_or_telephone')
        password = request.POST.get('password')

        user = authenticate(request, username=email_or_telephone, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                
                if user.is_superuser:
                    return redirect('dashboard')
                else:
                    return redirect('video-list')
            else:
                messages.error(request, "Your account is not active. Please contact the administrator.")
        else:
            messages.error(request, "username or password are incorrect. Please try again.")

    return render(request, 'accounts/login.html')



def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        # Delete the user
        user.delete()
        return redirect('user_list')  # Redirect to a page displaying the list of users
    
    return render(request, 'accounts/delete_user.html', {'user': user})


def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        email = request.POST['email']
        full_name = request.POST.get('full_name', '')
        telephone = request.POST.get('telephone', '')
        # Update user details
        user.email = email
        user.full_name = full_name
        user.telephone = telephone
        user.save()


        return redirect('user_list')

    return render(request, 'accounts/edit_user.html', {'user': user})