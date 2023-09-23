from django.urls import path
from .views import VideoListView, VideoDetailView,VideoListCreateView, dashboard

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('video/create', VideoListCreateView.as_view(), name='video-list-create'),
    path('video/<int:pk>/watch/', VideoDetailView.as_view(), name='video-watching'),
    path('dashboard/', dashboard, name='video-watching'),

    
    
]
