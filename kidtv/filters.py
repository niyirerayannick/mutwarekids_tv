import django_filters
from .models import Video

class VideoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')  # Case-insensitive search by title

    class Meta:
        model = Video
        fields = ['title', 'category']  # Add other fields as needed
