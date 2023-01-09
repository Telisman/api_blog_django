from django.contrib import admin
from api.models import Post,Category



# add moduls to are django dashboard page, for managing
admin.site.register(Post)
admin.site.register(Category)