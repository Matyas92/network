from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='profile',related_name='profile', on_delete=models.CASCADE)
    follower = models.ManyToManyField('User',  related_name='follower', blank=True)
    follows = models.ManyToManyField('User',  related_name='follows',  blank=True)

    def __str__(self):
        return str(self.user) 

def createProfile(sender,instance,created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            
        )    

post_save.connect(createProfile, sender=User)



class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    likefrom = models.ManyToManyField(User, blank = True, related_name='likeform')

    def __str__(self):
        return self.title 


