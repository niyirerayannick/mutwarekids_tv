
from rest_framework import generics, filters
from django.shortcuts import render, redirect
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


