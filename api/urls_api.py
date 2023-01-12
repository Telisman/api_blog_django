# url file for api views
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    # List of API calls
    path('api_calls/', views.api_calls, name='api_calls'),

    # User Serializers urls
    path('users/', views.UserList.as_view(),name='api_users'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-token-auth/', views.api_detail_blog_view),
    path('api-token-auth/edit/<int:pk>', views.api_update_blog_view),
    path('api-token-auth/delete/<int:pk>', views.api_delete_blog_view),
    path('create', views.api_create_blog_view),
    path('register', views.register_view),

    # Category Serializer urls
    path('category/', views.CategoryList.as_view(),name='category_name'),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),

    # Blog Serializer urls
    path('posts/', views.PostList.as_view(),name='api_posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),

    #User token
    path('api-token-auth/token', views.CustomAuthTokenLogin.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)