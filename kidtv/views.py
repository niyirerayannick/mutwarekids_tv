
from rest_framework import generics, filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer



class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category']

class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view_count()  # Custom method to increment video views
        instance.save()  # Save the updated instance
        serializer = self.get_serializer(instance)
        return Response({
            'video_details': serializer.data,
            'message': 'Video is now being watched.'
        }, status=status.HTTP_200_OK)

class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


def dashboard(request):
    return render(request, "accounts/dashboard.html")