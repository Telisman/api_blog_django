# rest_framework library
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions,authentication
from rest_framework.permissions import IsAuthenticated

# import function and models from are project
from .forms import NewUserForm,AddBlog
from .serializers import PostSerializer,UserSerializer,CategorySerializer,RegisterSerializer
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




# Set GET,PUT,DELETE API page with promision
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_blog_view(request):

    try:
        blog_post = Post.objects.get()
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializers = PostSerializer(blog_post)
        return Response(serializers.data)

@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_blog_view(request,pk):
    try:
        blog_post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.owner != user:
        return Response({'response': "You don't have permission to edit this"})

    if request.method == "PUT":
        serializers = PostSerializer(blog_post,data=request.data)
        data ={}
        if serializers.is_valid():
            serializers.save()
            data["success"] = "update successful"
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_blog_view(request,pk):
    try:
        blog_post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.owner != user:
        return Response({'response': "You don't have permission to delete this"})

    if request.method == "DELETE":
        operation = blog_post.delete()
        data ={}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request,*args, **kwargs):
    user_id = request.user
    blog_post= Post(owner=user_id)
    if request.method == "POST":
        serializers = PostSerializer(blog_post, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def register_view(request):
    if request.method == "POST":
        serializers = RegisterSerializer(data=request.data)
        data = {}
        if serializers.is_valid():
            user = serializers.save()
            data['respones'] ="Thx for register"
            data['username'] =user.username
        else:
            data = serializers.errors
        return Response(data)

# We can set POST,PUT,GET and DELETE on same function to sort are code better, for now I am using this type of code for better understanding



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
