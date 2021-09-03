from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm

User = get_user_model()


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "final_project_app/register.html", {'form': form})

    def get(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create(name=form.changed_data['name'], password=form.cleaned_data['password'])
            return redirect('/home')
        else:
            return render(request, "final_project_app/register.html", {'form': form})
