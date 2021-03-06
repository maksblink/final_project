"""final_project_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from final_project_app.views import HomeView, RegisterView, LoginView, LogoutView, ChangePasswordView, \
    ChooseTheOptionsView, PlayView, GamesDetailsView, GamesView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', HomeView.as_view(), name="home"),
    re_path(r'^home/$', HomeView.as_view(), name="home"),
    re_path(r'^register/$', RegisterView.as_view(), name="register"),
    re_path(r'^login/$', LoginView.as_view(), name="log_in"),
    re_path(r'^logout/$', LogoutView.as_view(), name="log_out"),
    re_path(r'^change_password/(?P<user_id>\d+)/$', ChangePasswordView.as_view(), name="change_password"),
    re_path(r'^choose_the_options/(?P<user_id>\d+)/$', ChooseTheOptionsView.as_view(), name="choose_options"),
    re_path(r'^play/(?P<game_id>\d+)/$', PlayView.as_view(), name="play"),
    re_path(r'^games_details/(?P<game_id>\d+)/$', GamesDetailsView.as_view(), name="game_details"),
    re_path(r'^games/(?P<user_id>\d+)/$', GamesView.as_view(), name="games"),
]
