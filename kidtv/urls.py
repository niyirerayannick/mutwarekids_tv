from django.urls import path
from .views import VideoListView, VideoDetailView,add_video, home

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('video/create',add_video, name='video-create'),
    path('video/<int:pk>/watch/', VideoDetailView.as_view(), name='video-watching'),
    path('', home, name='video-watching'),

    
    
    
]
