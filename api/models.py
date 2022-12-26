from django.db import models
from django.urls import reverse


class Category(models.Model):
    # id = models.AutoField(primary_key=True, editable=False)
    category_name = models.CharField(max_length=50,default='')
    def __str__(self):
        return self.category_name

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

