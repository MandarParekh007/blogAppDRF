from django.db import models
from users.models import CustomUser
from django.utils.timezone import now

class Tags(models.Model):
    tag = models.CharField(max_length=20)
    # blog_id = models.ForeignKey(Blogs, on_delete=models.CASCADE ,blank=False)
    
    def __str__(self):
        return self.tag

# Create your models here.
class Blogs(models.Model):
    title = models.CharField(max_length=100)
    publish_date = models.DateField(default=now)
    author = models.ForeignKey(CustomUser, related_name='author_id', on_delete=models.CASCADE, blank=False)
    content = models.TextField(max_length=500)
    isDraft = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)
    def __str__(self):
        return self.title

    
class Comments(models.Model):
    comment = models.CharField(max_length=200)
    blog_id = models.ForeignKey(Blogs, on_delete=models.CASCADE, blank=False)
    user_id = models.ForeignKey(CustomUser,related_name='user_id', on_delete=models.CASCADE, blank=False)
    
