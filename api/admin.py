from django.contrib import admin
from api.models import Post,Category
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


# add moduls to are django dashboard page, for managing
admin.site.register(Post)
admin.site.register(Category)