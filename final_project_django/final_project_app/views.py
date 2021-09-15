from random import randint

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, LoginForm, ChangePasswordForm, OptionsForm, PlayForm
from .models import Game, GameAnswers

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
                              {'form': form, 'error': 'This user already exists.'})
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


class ChangePasswordView(View):
    def get(self, request, user_id):
        form = ChangePasswordForm()
        return render(request, 'final_project_app/change_password.html', {'form': form})

    def post(self, request, user_id):
        form = ChangePasswordForm(request.POST)
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return render(request, 'final_project_app/change_password.html',
                          {'form': form, 'error': 'User with this id does not exist.'})
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/home')
        else:
            return render(request, 'final_project_app/change_password.html', {'form': form})


class ChooseTheOptionsView(View):
    def get(self, request):
        form = OptionsForm()
        return render(request, 'final_project_app/confirm_options.html', {'form': form})

    def post(self, request):
        form = OptionsForm(request.POST)

        if form.is_valid():
            game = Game.objects.create(operator=form.cleaned_data['operation'],
                                       range1_min=form.cleaned_data['minimum_number_of_first_factor'],
                                       range1_max=form.cleaned_data['maximum_number_of_first_factor'],
                                       range2_min=form.cleaned_data['minimum_number_of_second_factor'],
                                       range2_max=form.cleaned_data['maximum_number_of_second_factor'])
            return redirect('play', game_id=game.id)
        else:
            return render(request, 'final_project_app/confirm_options.html', {'form': form})


class PlayView(View):
    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        first = randint(game.range1_min, game.range1_max)
        second = randint(game.range2_min, game.range2_max)
        op = game.operator
        if op == "+":
            correct_answer = first + second
        elif op == "-":
            correct_answer = first - second
        elif op == "*":
            correct_answer = first * second
        elif op == "/":
            correct_answer = first / second
        elif op == "%":
            correct_answer = first % second
        answer = GameAnswers.objects.create(first_factor=first, second_factor=second, game=game,
                                            correct_answer=correct_answer)
        form = PlayForm({'answer_id': answer.id})
        ctx = {
            'form': form,
            'operator': op,
            'first': first,
            'second': second
        }
        return render(request, 'final_project_app/play.html', ctx)

    def post(self, request, game_id):
        form = PlayForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            if user_answer is None:  # or "e" in user_answer:  # we need to make the validation for format "1e1"
                form.add_error('answer', "This field is required.")
                ctx = {
                    'form': form,
                    'operator': request.POST.get('operator'),
                    'first': request.POST.get('first'),
                    'second': request.POST.get('second')
                }
                return render(request, 'final_project_app/play.html', ctx)
            object_answer = GameAnswers.objects.get(pk=form.cleaned_data['answer_id'])
            object_answer.answer = user_answer
            object_answer.save()
            game = Game.objects.get(pk=game_id)
            if user_answer == object_answer.correct_answer:
                game.number_of_correct_answers += 1
                object_answer.was_this_answer_correct = True
            else:
                game.number_of_wrong_answers += 1
                object_answer.was_this_answer_correct = False
            game.save()
            return redirect('play', game_id=game_id)
        else:
            ctx = {
                'form': form,
                'operator': request.POST.get('operator'),
                'first': request.POST.get('first'),
                'second': request.POST.get('second')
            }
            return render(request, 'final_project_app/play.html', ctx)


class StopPlayView(View):
    def get(self, request, game_id):
        pass

    def post(self, request, game_id):
        pass
