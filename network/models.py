from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # following = models.ManyToManyField("self", related_name="following", default=None, blank=True, symmetrical=False)
    followers = models.ManyToManyField("self", related_name="following", default=None, blank=True, symmetrical=False)

    def serialize(self):

        return {
            "id": self.id,
            "username": self.username,
            "following": [user.username for user in self.following.all()],
            "following_count": self.following.count(),
            "followers": [user.username for user in self.followers.all()],
            "followers_count": self.followers.count()
        }
    

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked", default=None)

    def __str__(self):
        return f"{self.creator} wrote: {self.content}"

    def serialize(self):
        
        return {
            "id": self.id,
            "author": self.creator.username,
            "content": self.content,
            "date": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "liked_by": [user.username for user in self.liked_by.all()]
        }


