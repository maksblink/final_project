from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
