from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True)
    linkedin_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def avatar_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            # return "https://res.cloudinary.com/dmphcbabx/image/upload/v1760011712/default_uhnzmo.svg"
            return "https://res.cloudinary.com/dmphcbabx/image/upload/v1760011808/default_ycnnid.svg"