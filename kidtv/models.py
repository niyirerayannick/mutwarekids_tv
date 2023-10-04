from django.db import models
from core.models import CustomUser

class Video(models.Model):

    CATEGORY_CHOICES = [
        ('animation', 'Animation'),
        ('podcast', 'Podcast'),
        ('number', 'Number'),
        ('myfamiy', 'Myfamily'),
        ('alphabetic', 'Alphabetic'),
        ('myhome', 'Myhome'),



        
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/file')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    banner =  models.FileField(upload_to='videos/banner')
    upload_date = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)  # Add view count field

    def __str__(self):
        return self.title

    def increment_view_count(self):
        self.view_count += 1
        self.save()
