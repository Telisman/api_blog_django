from rest_framework import generics
from api import serializers
from django.contrib.auth.models import User
from api.models import Post
from rest_framework import permissions,authentication
from api.permissions import IsOwnerOrReadOnly
from django.shortcuts import render, redirect
from .forms import NewUserForm,AddBlog
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import UpdateView,DetailView, DeleteView




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
                messages.success(request ,'Account has been created succesfully')
                return redirect('logandreg')
            else:
                messages.error(request ,form.errors)
                return redirect('logandreg')
        return render(request ,'loginandregister.html')

def logout_user(request):
    logout(request)
    messages.success(request,('You are logout'))
    return redirect('logandreg')

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


def blog(request):
    blog_post= Post.objects.all()
    context = {
        'blog_post': blog_post,
    }
    return render(request, 'blog.html', context)


class BlogDetailView(DetailView):
    model = Post
    template_name = "blog_detail.html"



class UpdateViewBlog(UpdateView):
    model = Post
    template_name = "update_blog.html"
    fields = ['title','body']


def AddNewBlog(request):
    submitted = False
    if request.method == "POST":
        form = AddBlog(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'blog.html')
    else:
        pass

    form = AddBlog
    return render(request, "add_blog.html", {'form': form})

class DeleteBlog(DeleteView):
    model = Post
    template_name = "delete_blog.html"
    success_url = reverse_lazy('blog')
