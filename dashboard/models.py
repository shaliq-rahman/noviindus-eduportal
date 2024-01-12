from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=250, blank=True)
    subtitle = models.CharField(max_length=250, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='course_images', blank=True, null=True)
    is_active = models.BooleanField("Active",default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    
    def __str__(self):
        return self.title
