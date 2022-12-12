from django.urls import path,include
from .views import HomePageView

urlpatterns = [
    path('Housemaster/', HomePageView, name='housemaster'),
]