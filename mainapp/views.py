from django.shortcuts import render,get_object_or_404
from django.views import View
from .forms import userForm,loginForm,submitBlogForm,submitCommentForm
from .models import User,BlogPost,CommentPost,Tag
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection


# Create your views here.

class signupView(View):
    """
    View to control the signup process
    """
    templateName = 'mainapp/signup.html'

    def get(self, request):                                #GET response for signup url
        userDetails = userForm()

        return render(request,self.templateName,{'userDetails':userDetails})

    def post(self, request):                               #POST repsonse for signup url
        userDetails = userForm(request.POST)
        if userDetails.is_valid():
            u = userDetails.save(commit=False)
            user = User.objects.create_user(u.username,u.email,u.password,first_name=u.first_name,last_name=u.last_name)
            user.save()
            return HttpResponseRedirect(reverse('mainapp:login'))
        else:
            return render(request,self.templateName,{'userDetails':userDetails})

class loginView(View):
    """
    View to control the login process
    """
    templateName = 'mainapp/login.html'

    def get(self,request):                                   #GET response for login url
        loginDetails = loginForm()
        return render(request, self.templateName, {'loginDetails':loginDetails})
    def post(self,request):                                  #POST responsefor login url
        loginDetails = loginForm(request.POST)
        if loginDetails.is_valid():
            username = loginDetails.cleaned_data['username']
            password = loginDetails.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('mainapp:home'))
            else:
                loginDetails.add_error(None,'Username and password doesn\'t match')
                return render(request, self.templateName, {'loginDetails' : loginDetails})

        else:
            return render(request, self.templateName, {'loginDetails' : loginDetails})

class homeView(LoginRequiredMixin,View):
    templateName = 'mainapp/home.html'
    login_url = 'mainapp:login'
    def get(self,request):
        postObjects = BlogPost.objects.all()
        if request.GET.get('q',None):
            postObjects = postObjects.filter(tags=Tag.objects.get(name=request.GET['q']))
        cur = connection.cursor()
        cur.callproc('getnotification',[request.user.id])
        results = cur.fetchall()
        cur.close()
        notifObjects = [CommentPost.objects.get(id=x[0]) for x in results]


        return render(request,self.templateName,{'postObjects':postObjects,'notifObjects':notifObjects})

class submitBlogView(LoginRequiredMixin,View):
    templateName = 'mainapp/blog.html'
    login_url = 'mainapp:login'
    def get(self,request):
        blogDetails = submitBlogForm()
        return render(request,self.templateName,{'blogDetails':blogDetails})
    def post(self,request):
        blogDetails = submitBlogForm(request.POST)
        if blogDetails.is_valid():
            post = blogDetails.save(commit=False)
            post.author = request.user
            post.save()
            post.tags.set(blogDetails.cleaned_data['tags'])
            #blogDetails.save_m2m()
            return HttpResponseRedirect(reverse('mainapp:blog',kwargs={'num':int(post.id)}))
        else:
            return render(request,self.templateName,{'blogDetails':blogDetails})


class blogView(LoginRequiredMixin,View):
    templateName = 'mainapp/blogView.html'
    login_url = 'mainapp:login'
    def get(self,request,num):
        post = get_object_or_404(BlogPost,pk=num)
        comments = CommentPost.objects.filter(postId=int(num))
        commentDetails = submitCommentForm()
        return render(request,self.templateName,{'post':post,'commentDetails':commentDetails,
                                                 'comments':comments})
    def post(self,request,num):
        commentDetails = submitCommentForm(request.POST)
        postId = get_object_or_404(BlogPost, pk=num)
        comments = CommentPost.objects.filter(postId=int(num))
        if commentDetails.is_valid():
            comment = commentDetails.save(commit=False)
            comment.postId = postId
            comment.author = request.user
            comment.save()
            return HttpResponseRedirect(reverse('mainapp:blog',kwargs={'num':int(num)}))
        else:
            return render(request,self.templateName,{'post':postId,
                                                     'commentDetails':commentDetails,
                                                     'comments': comments})

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:login'))

def notifs(user):
    c=connection.cursor()
    c.callproc('getnotification',[user,])
    results = c.fetchall()
    print(user,results)
    c.close()
    return [CommentPost.objects.get(id=x[0]) for x in results]




def success(request):
    return HttpResponse('Success!')