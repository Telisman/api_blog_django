from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from .views import LoginView,blog,BlogDetailView,UpdateViewBlog,logout_user,AddNewBlog,DeleteBlog

urlpatterns = [
    path('users/', views.UserList.as_view(),name='api_users'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-token-auth/', views.api_detail_blog_view),
    path('api-token-auth/edit/<int:pk>', views.api_update_blog_view),
    path('api-token-auth/delete/<int:pk>', views.api_delete_blog_view),
    path('create', views.api_create_blog_view),
    path('register', views.register_view),


    path('category/', views.CategoryList.as_view(),name='category_name'),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),

    path('posts/', views.PostList.as_view(),name='api_posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),

    path('logandreg/', include('django.contrib.auth.urls')),
    path('logandreg/', LoginView.as_view(), name='logandreg'),
    path('logout/', logout_user, name='logout'),

    path('blog/', include('django.contrib.auth.urls')),
    path('blog/', blog, name='blog'),
    path('blog/addBlog', include('django.contrib.auth.urls')),
    path('blog/addBlog/', AddNewBlog, name='add_blog'),
    path('blog/detail', include('django.contrib.auth.urls')),
    path('blog/detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/detail/edit/<int:pk>', UpdateViewBlog.as_view(), name='update_blog'),
    path('blog/detail/<int:pk>/remove', DeleteBlog.as_view(), name='delete_blog'),
]

urlpatterns = format_suffix_patterns(urlpatterns)