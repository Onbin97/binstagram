from django.db import models

from users.models import User
from utils.models import TimestampZone

class Post(TimestampZone):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(null=True)
    
    class Meta:
        db_table = "posts"

class Image(TimestampZone):
    image_url = models.CharField(max_length=2000)
    post      = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    
    class Meta:
        db_table = "images"

class Comments(TimestampZone):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=2000)

    class Meta:
        db_table = "comments"