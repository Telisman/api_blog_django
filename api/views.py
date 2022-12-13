from rest_framework import generics
from api import serializers
from django.contrib.auth.models import User
from api.models import Post
from rest_framework import permissions,authentication
from api.permissions import IsOwnerOrReadOnly
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.views import View




class LoginView(View):
    def get(self ,request):
        form = NewUserForm()
        if "sign-in" in request.GET:
            username = request.GET.get("username")
            password = request.GET.get("pswd")
            user = authenticate(username=username ,password=password)
            if user is not None:
                login(request ,user)
                return redirect('home')
            else:
                messages.info(request ,'Login attemp failed.')
                return redirect('logandreg')
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







# def register_login(request):
#     if request.method == "POST":
#         if 'login' in request.POST:
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 return redirect('login')
#
#
#         elif 'register' in request.POST:
#             form = NewUserForm()
#             if form.is_valid():
#                 user = form.save()
#                 login(request, user)
#                 messages.success(request, "Registration successful.")
#                 return render(request,template_name="loginandregister.html")
#             messages.error(request, "Unsuccessful registration. Invalid information.")
#
#     form = NewUserForm()
#     return render(request=request, template_name="loginandregister.html", context={"register_form": form})
#


    # if request.method == "POST":
    #     form = NewUserForm(request.POST)
    #     if "register" in request.method == "POST":
    #         if form.is_valid():
    #             user = form.save()
    #             login(request, user)
    #             messages.success(request, "Registration successful.")
    #             return render(request,template_name="loginandregister.html")
    #         messages.error(request, "Unsuccessful registration. Invalid information.")
    #
    #     if "login" in request.method == "POST":
    #
            # username = request.POST['username']
            # password = request.POST['password']
            # user = authenticate(request, username=username, password=password)
            # if user is not None:
            #     login(request, user)
            #     return redirect('home')
            # else:
            #     return redirect('login')
    # form = NewUserForm()
    # return render(request=request, template_name="loginandregister.html", context={"register_form": form})
    #
    #


# def register_request(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful.")
#             return render(request,template_name="loginandregister.html")
#         messages.error(request, "Unsuccessful registration. Invalid information.")
#
    # form = NewUserForm()
    # return render(request=request, template_name="loginandregister.html", context={"register_form": form})
#
#
# def login_request(request):
#         if request.method == "POST":
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#         else:
#             return redirect('login')
#         return render(request, "home.html", {})

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