from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from faker import Faker

faker = Faker("pl_PL")


def add_permissions(fake_user):
    normal_user_group = Group.objects.get(name='normal_users')
    normal_user_group.user_set.add(fake_user)


def fake_user_data():
    return {
        "password": faker.name(),
        "username": faker.name(),
        "first_name": faker.name(),
        "last_name": faker.name(),
        "email": faker.email(),
    }


def fake_user_data_for_sign_up():
    data = fake_user_data()
    data["password_again"] = data["password"]
    return data


def create_fake_user():
    fake_user = User.objects.create_user(**fake_user_data())
    add_permissions(fake_user)


def create_fake_group():
    Group.objects.get_or_create(name='normal_users')
