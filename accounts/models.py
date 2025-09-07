from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    theme_preference = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')

    def __str__(self):
        return f"{self.user.username} - {self.theme_preference}"