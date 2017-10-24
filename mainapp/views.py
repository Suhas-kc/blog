from django.shortcuts import render
from django.views import View
from .forms import userForm,loginForm
from .models import User
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse



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
                return HttpResponseRedirect(reverse('mainapp:success'))
            else:
                loginDetails.add_error(None,'Username and password doesn\'t match')
                return render(request, self.templateName, {'loginDetails' : loginDetails})

        else:
            return render(request, self.templateName, {'loginDetails' : loginDetails})

class homeView(View):
    templateName = 'mainapp/home.html'
    def get(self,request):
        return render(request,self.templateName)

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:login'))


def success(request):
    return HttpResponse('Success!')