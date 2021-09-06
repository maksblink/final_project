from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, LoginForm

User = get_user_model()


class HomeView(View):
    def get(self, request):
        return render(request, "final_project_app/base.html")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "final_project_app/register.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                new_user = User.objects.create_user(password=form.cleaned_data['password'],
                                                    username=form.cleaned_data['username'],
                                                    first_name=form.cleaned_data['first_name'],
                                                    last_name=form.cleaned_data['last_name'],
                                                    email=form.cleaned_data['email'])
            except IntegrityError:
                return render(request, "final_project_app/register.html",
                              {'form': form, 'error': 'This user is already exist.'})
            normal_user_group = Group.objects.get(name='normal_users')
            normal_user_group.user_set.add(new_user)
            return redirect('/home')
        else:
            return render(request, "final_project_app/register.html", {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "final_project_app/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/home')
            else:
                return render(request, "final_project_app/login.html",
                              {'form': form, 'error': "Incorrect login or password."})
        else:
            return render(request, "final_project_app/login.html", {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/home')
