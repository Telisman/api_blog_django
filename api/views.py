# rest_framework library
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions,authentication

# import function and models from are project
from .forms import NewUserForm,AddBlog
from .serializers import PostSerializer,UserSerializer,CategorySerializer
from api.models import Post,Category
from api.permissions import IsOwnerOrReadOnly


#django library
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import UpdateView,DetailView, DeleteView
from django.contrib.auth.models import User




# Exemple of serializers show blog API
@api_view(['GET', ])
def api_detail_blog_view(request):

    try:
        blog_post = Post.objects.get()
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializers = PostSerializer(blog_post)
        return Response(serializers.data)

@api_view(['PUT', ])
def api_update_blog_view(request,pk):

    try:
        blog_post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializers = PostSerializer(blog_post,data=request.data)
        data ={}
        if serializers.is_valid():
            serializers.save()
            data["success"] = "update successful"
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE', ])
def api_delete_blog_view(request,pk):

    try:
        blog_post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = blog_post.delete()
        data ={}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


@api_view(['POST', ])
def api_create_blog_view(request):
    account = User.objects.get(username = "DavorTelisman")
    blog_post= Post(owner=account)
    if request.method == "POST":
        serializers = PostSerializer(blog_post, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




# Login and registration view
class LoginView(View):
    def get(self ,request):
        form = NewUserForm()
        if "sign-in" in request.GET:
            username = request.GET.get("username")
            password = request.GET.get("pswd")
            user = authenticate(username=username ,password=password)
            if user is not None:
                login(request ,user)
                return redirect('blog')
            else:
                messages.info(request ,'Login attemp failed.')
                return redirect('blog')
        return render(request ,'loginandregister.html' ,{'form' :form})

    def post(self ,request):
        if "sign-up" in request.POST:
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return render(request,'blog.html',{ "info":"Registration successful!" + " New user created: " + request.POST.get('username')})
            else:
                messages.error(request ,form.errors)
                return redirect('logandreg')
        return render(request ,'loginandregister.html')



# Logout view
def logout_user(request):
    logout(request)
    messages.success(request,('You are logout'))
    return redirect('logandreg')



# Users api view: display list of users and users detail
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Post api view: display list of posts and posts detail

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class =PostSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


# Category api view: display list of Category and Categorys detail
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# blog view page: display all blogs
def blog(request):
    blog_post= Post.objects.all()
    context = {
        'blog_post': blog_post,
    }
    return render(request, 'blog.html', context)

# display blogs detail
class BlogDetailView(DetailView):
    model = Post
    template_name = "blog_detail.html"


# Update blog page using django UpdateView
class UpdateViewBlog(UpdateView):
    model = Post
    template_name = "update_blog.html"
    fields = ['title','body','category']



# Add new blog page, using form AddBlog
def AddNewBlog(request):
    submitted = False
    if request.method == "POST":
        form = AddBlog(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'add_blog.html',{"info":"You created new blog"})
    else:
        pass

    form = AddBlog
    return render(request, "add_blog.html", {'form': form})

# Delete blog page: DeleteView
class DeleteBlog(DeleteView):
    model = Post
    template_name = "delete_blog.html"
    success_url = reverse_lazy('blog')
