# URL file for blog view web page

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LoginView,blog,BlogDetailView,UpdateViewBlog,logout_user,AddNewBlog,DeleteBlog

urlpatterns = [
    # Login and Registration urls
    path('logandreg/', include('django.contrib.auth.urls')),
    path('logandreg/', LoginView.as_view(), name='logandreg'),
    path('logout/', logout_user, name='logout'),

    # Blog display urls
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