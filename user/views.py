from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from .forms import LoginForm
from .forms import RegisterForm
from django.contrib.auth.models import User

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        loginform = LoginForm(data=request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data.get('username')
            password = loginform.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  
                return redirect('home')  
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin')

    else:
        loginform = LoginForm()  

    return render(request, 'login.html', {"form": loginform})

def register_view(request):
    if request.method == 'POST':
        registerform = RegisterForm(data=request.POST)
        if registerform.is_valid():
            username = registerform.cleaned_data.get('username')
            email = registerform.cleaned_data.get('email')
            password = registerform.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Đăng ký thành công')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin')
    return render(request,'register.html',{"form":RegisterForm()})

def logout_view(request):
    logout(request)
    return redirect('home')