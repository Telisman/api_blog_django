from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token





# Category model
class Category(models.Model):
    # id = models.AutoField(primary_key=True, editable=False)
    category_name = models.CharField(max_length=50,default='')
    def __str__(self):
        return self.category_name


# Blog Model
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category',null=True,on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog')

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


# Automatically create user token for every new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)