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
                new_user = User.objects.create_user(password=request.POST.get('password'),
                                                    username=request.POST.get('username'),
                                                    first_name=request.POST.get('first_name'),
                                                    last_name=request.POST.get('last_name'),
                                                    email=request.POST.get('email'))
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
    def get(self, request, user_id):
        form = OptionsForm()
        return render(request, 'final_project_app/confirm_options.html', {'form': form})

    def post(self, request, user_id):
        form = OptionsForm(request.POST)

        if form.is_valid():
            game = Game.objects.create(operator=form.cleaned_data['operation'],
                                       range1_min=form.cleaned_data['minimum_number_of_first_factor'],
                                       range1_max=form.cleaned_data['maximum_number_of_first_factor'],
                                       range2_min=form.cleaned_data['minimum_number_of_second_factor'],
                                       range2_max=form.cleaned_data['maximum_number_of_second_factor'],
                                       user=User.objects.get(pk=user_id))
            return redirect('play', game_id=game.id)
        else:
            return render(request, 'final_project_app/confirm_options.html', {'form': form})


class PlayView(View):
    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        answer_possible_wrong = game.gameanswers_set.last()
        if answer_possible_wrong is None:
            class FakeObj:
                def __init__(self, answer):
                    self.answer = answer

            answer_possible_wrong = FakeObj("fake_answer")
        if answer_possible_wrong.answer is None:
            answer = answer_possible_wrong
            form = PlayForm({'answer_id': answer.id})
            ctx = {
                'form': form,
                'operator': game.operator,
                'first': answer.first_factor,
                'second': answer.second_factor,
                'answer_id': answer.id
            }
        else:
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
                'second': second,
                'answer_id': answer.id
            }
        return render(request, 'final_project_app/play.html', ctx)

    def post(self, request, game_id):
        form = PlayForm(request.POST)
        if form.is_valid():
            stop = request.POST.get('btn')
            object_answer = GameAnswers.objects.get(pk=form.cleaned_data['answer_id'])
            if stop == 'Stop':
                object_answer.delete()
                return redirect('stop_play', game_id=game_id)
            user_answer = form.cleaned_data['answer']
            if user_answer is None:
                form.add_error('answer', "This field is required.")
                ctx = {
                    'form': form,
                    'operator': request.POST.get('operator'),
                    'first': request.POST.get('first'),
                    'second': request.POST.get('second'),
                    'answer_id': request.POST.get('answer_id'),
                    'error': "This field is required."
                }
                return render(request, 'final_project_app/play.html', ctx)
            object_answer.answer = user_answer
            game = Game.objects.get(pk=game_id)
            if user_answer == object_answer.correct_answer:
                game.number_of_correct_answers += 1
                object_answer.was_this_answer_correct = True
            else:
                game.number_of_wrong_answers += 1
                object_answer.was_this_answer_correct = False
            object_answer.save()
            game.save()
            return redirect('play', game_id=game_id)
        else:
            ctx = {
                'form': form,
                'operator': request.POST.get('operator'),
                'first': request.POST.get('first'),
                'second': request.POST.get('second'),
                'answer_id': request.POST.get('answer_id'),
                'error': "This is not valid a number."
            }
            return render(request, 'final_project_app/play.html', ctx)


class StopPlayView(View):
    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        game.is_game_ended = True
        game.save()
        correct_answers = game.number_of_correct_answers
        wrong_answers = game.number_of_wrong_answers
        try:
            precision = round(correct_answers / (correct_answers + wrong_answers) * 100, 2)
        except ZeroDivisionError:
            precision = 0.0

        ctx = {
            'operator': game.operator,
            'range1_min': game.range1_min,
            'range1_max': game.range1_max,
            'range2_min': game.range2_min,
            'range2_max': game.range2_max,
            'number_of_correct_answers': correct_answers,
            'number_of_wrong_answers': wrong_answers,
            'precision': precision,
            'user_id': game.user,
        }
        return render(request, 'final_project_app/stop_play.html', ctx)


class GamesView(View):
    def get(self, request, user_id):
        games = Game.objects.filter(user=user_id)
        return render(request, 'final_project_app/games.html', {'games': games})


class AnswersView(View):
    def get(self, request, game_id):
        answers = GameAnswers.objects.filter(game=game_id)
        return render(request, 'final_project_app/answers.html', {'answers': answers})
