from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

class RegisterView(View):
    def get(self, request):
        return render(request,'users/register.html')

    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password == password2:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email)
            user.set_password(password)
            user.save()
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request,'users/login.html')