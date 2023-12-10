from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_varified = models.BooleanField(default=False)
    code = models.IntegerField()
    profile_img = models.ImageField(upload_to='profile_image' , blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    mesg = models.TextField(max_length=200)

    def __str__(self):
        return self.username


class Categorise(models.Model):
    name = models.CharField(max_length=100, default="Computer Engineering")
    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    caty = models.ForeignKey(Categorise,on_delete=models.CASCADE, null=True)
    img =models.ImageField(upload_to='post_img',blank= True)
    title = models.CharField(max_length=200)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True,blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.user)




