from django.contrib.auth.models import AbstractUser
#from .cheer import settings

class CustomUser(AbstractUser):
    def __str__(self):
        return self.email
