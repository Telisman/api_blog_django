from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from .views import LoginView,blog,BlogDetailView,UpdateViewBlog

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('logandreg/', include('django.contrib.auth.urls')),
    path('logandreg/', LoginView.as_view(), name='logandreg'),
    path('blog/', blog, name='blog'),
    path('blog/detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/detail/edit/<int:pk>', UpdateViewBlog.as_view(), name='update_blog'),
]

urlpatterns = format_suffix_patterns(urlpatterns)