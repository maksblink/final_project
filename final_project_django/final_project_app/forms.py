import django.forms as forms
from django.core.exceptions import ValidationError


# def passwords(clean):
#     cleaned_data = super().clean()
#     if cleaned_data['password'] != cleaned_data['password_again']:
#         raise ValidationError('Passwords do not match.')
#     return cleaned_data


class RegisterForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    # def clean(self):
    #     passwords(self)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_again']:
            raise ValidationError('Passwords do not match.')
        return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='New password.', widget=forms.PasswordInput)
    password_again = forms.CharField(label='Repeat password.', widget=forms.PasswordInput)

    # def clean(self):
    #     passwords(self)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_again']:
            raise ValidationError('Passwords do not match.')
        return cleaned_data
