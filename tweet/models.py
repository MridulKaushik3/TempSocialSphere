from django.db import models
from django.contrib.auth.models import User

TONE_CHOICES = [
    ('neutral', 'Neutral'),
    ('toxic', 'Toxic'),
    ('non-toxic', 'Non-Toxic'),
]

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='tweets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tone = models.CharField(max_length=10, choices=TONE_CHOICES, default='neutral')

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'

    @property
    def like_count(self):
        return self.likes.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'tweet')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked Tweet {self.tweet.id}"

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on Tweet {self.tweet.id}"
