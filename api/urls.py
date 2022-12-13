from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from .views import LoginView

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('logandreg/', include('django.contrib.auth.urls')),
    path('logandreg/', LoginView.as_view(), name='logandreg'),

]

urlpatterns = format_suffix_patterns(urlpatterns)