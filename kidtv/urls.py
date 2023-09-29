from django.urls import path
from core.views import login, register
from .views import VideoListView, VideoDetailView,add_video, home

urlpatterns = [
    path('', home, name='home'), 
    path('login', login, name='login'), 
    path('register', register, name='register'), 
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('video/create',add_video, name='video-create'),
    path('video/<int:pk>/watch/', VideoDetailView.as_view(), name='video-watching'),
    
]
