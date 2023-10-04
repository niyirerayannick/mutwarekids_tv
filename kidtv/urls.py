from django.urls import path
from core.views import adminlogin, register
from .views import VideoListView, VideoDetailView,add_video, home, RelatedVideosByCategory

urlpatterns = [
    path('home', home, name='home'), 
    path('mutware', adminlogin, name='login'), #this is for administrator login
    path('register', register, name='register'), 
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('video/create',add_video, name='video-create'),
    path('video/<int:pk>/watch/', VideoDetailView.as_view(), name='video-watching'),
    path('related/<str:category>/', RelatedVideosByCategory.as_view(), name='related-videos-by-category'),
    
]
