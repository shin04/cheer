from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    achievement = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def achieve(self):
        self.achievement = True
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('cheer_app.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
