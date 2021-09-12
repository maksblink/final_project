import django.forms as forms
from django.core.exceptions import ValidationError
from django.forms import RadioSelect


def passwords(cleaned_data):
    if cleaned_data['password'] != cleaned_data['password_again']:
        raise ValidationError('Passwords do not match.')
    return cleaned_data


class RegisterForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        return passwords(cleaned_data)


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='New password.', widget=forms.PasswordInput)
    password_again = forms.CharField(label='Repeat password.', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        return passwords(cleaned_data)


OPERATORS = (
    ('+', '+'),
    ('-', '-'),
    ('*', '*'),
    ('/', '/'),
    ('%', '%'),
)


class OptionsForm(forms.Form):
    operation = forms.ChoiceField(choices=OPERATORS, widget=RadioSelect())
    # number_of_fields = forms.IntegerField()
    maximum_number_of_first_factor = forms.IntegerField()
    minimum_number_of_first_factor = forms.IntegerField()
    maximum_number_of_second_factor = forms.IntegerField()
    minimum_number_of_second_factor = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['maximum_number_of_first_factor'] < cleaned_data['minimum_number_of_first_factor'] or \
                cleaned_data['maximum_number_of_second_factor'] < cleaned_data['minimum_number_of_second_factor']:
            raise ValidationError('The minimum number can not be greater than the maximum number.')
        return cleaned_data


class PlayForm(forms.Form):
    answer = forms.IntegerField()
