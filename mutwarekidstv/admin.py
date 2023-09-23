from django.contrib.admin import AdminSite
from django.shortcuts import render

class CustomAdminSite(AdminSite):

    def index(self, request, extra_context=None):
        # Create a custom dashboard view
        context = {
            'user_count': User.objects.count(),
            'video_count': Video.objects.count(),
        }
        return render(request, 'admin/dashboard.html', context)

# Register your custom admin site
mutware = CustomAdminSite(name='customadmin')
