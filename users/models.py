from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    """
    Model representing user profile information.

    Attributes:
        user (OneToOneField): Reference to the User model.
        bio (CharField): Optional biography of the user.
        profile_pic (ImageField): User's profile picture.
        is_teacher (BooleanField): Indicates if the user is a teacher.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(default='default.png', upload_to='profile_pics')
    is_teacher = models.BooleanField(default=False)


    def __str__(self):
        #String representation of the profile, shown as the username followed by "Profile".
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Override the save method to resize the profile picture before saving.
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        if img.height > 100 or img.width > 100:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


class Requests(models.Model):
    """
    Model representing user requests for a teacher account.

    Attributes:
        profile (ForeignKey): Reference to the user's Profile model.
        name (CharField): Name of the requester.
        email (EmailField): Email address of the requester.
        phone_number (CharField): Phone number of the requester.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        # String representation of the request, shown as the username of the requester followed by "Request".
        return f'{self.profile.user.username} Request'
