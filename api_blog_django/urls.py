from django.contrib import admin
from django.urls import path,include
from homepage.views import HomePageView
urlpatterns = [
    path('', HomePageView, name='home'),
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('api/', include('api.urls_api')),
    path('', include('django.contrib.auth.urls')),
]
