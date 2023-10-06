
from rest_framework import generics, filters
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from django.contrib.auth.decorators import login_required
from core.decorators import superuser_required 
from . import views
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category']

class VideoDetailView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view_count()  # Custom method to increment video views
        instance.save()  # Save the updated instance

        # Get related videos based on the category of the current video
        related_videos = Video.objects.filter(category=instance.category).exclude(id=instance.id)[:5]

        serializer = self.get_serializer(instance)
        related_serializer = VideoSerializer(related_videos, many=True)

        response_data = {
            'video_details': serializer.data,
            'related_videos': related_serializer.data,
            'message': 'Video is now being watched.'
        }

        return Response(response_data, status=status.HTTP_200_OK)


class RelatedVideosByCategory(APIView):
    def get(self, request, category):
        try:
            # Retrieve related videos by category
            related_videos = Video.objects.filter(category=category)[:5]  # Adjust the number of videos as needed
            serializer = VideoSerializer(related_videos, many=True, context={'request': request})

            serialized_data = serializer.data

            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@login_required  # Optional: You can also require the user to be logged in
@superuser_required  # Apply the custom decorator
def add_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        video_file = request.FILES['video_file']
        category = request.POST['category']
        banner = request.FILES['banner']

        # Create a new Video object and save it
        video = Video(title=title, description=description, video_file=video_file, category=category, banner=banner)
        video.save()

        return redirect('dashboard')  # Redirect to a page displaying the list of videos

    return render(request, 'accounts/add_video.html')





