from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from django.contrib.auth import login as auth_login ,logout as auth_logout ,authenticate
from.models import User


#
class signup(CreateView):
    model = User
    form_class = signup
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        return redirect('login')


def login(request):
    if request.method == "GET":
        return render(request,'login.html',{})

    elif request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('account')
def account(request):
    return render(request,'account_activation_email.html',{})
# @method_decorator(login_required(login_url='login'))
def profile(request):
    return render(request,'profile.html',{})

def logout(request):
    auth_logout(request)
    return redirect('login')



class AccountSttingView(UpdateView):
    model = User
    fields = ['first_name','last_name','profile_photo','facebook','country','birth_date']
    template_name = 'account_settings.html'
    success_url = '/profile/'
    def get_object(self, queryset=None):
        return self.request.user


# Create your views here.
