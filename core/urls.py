from django.urls import path
from .views import ( 
    UserRegistrationView, 
    UserLoginView, 
    ProfileView, 
    ProfileUpdateView,
    ChangePasswordView, 
    PasswordResetRequestView, 
    LogoutView, 
    dashboard, 
    video_list, 
    user_list,
    add_user,
    delete_video,
    edit_video,

    )

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/video_list', video_list, name='video_list'),
    path('dashiboard/user_list/', user_list, name='user_list'),
    path('dashboard/add_user/', add_user, name='add_user'),
    path('dashboard/video/<int:video_id>/edit/', edit_video, name='edit_video'),
    path('dashboard/video/<int:video_id>/delete/', delete_video, name='delete_video'),

    

]
