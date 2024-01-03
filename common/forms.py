from django import forms
from .models import Pictures
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import AuthenticationForm


class ImageForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = ('image',)


class Register(forms.Form):
    username = forms.CharField(
        max_length=70, 
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control', 'autofocus':True, 'type': 'text'})
    )
    email = forms.CharField(
        required=False,
        max_length=50, 
        widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'class': 'form-control', 'type': 'email'})
    )
    mob_phone = PhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile Phone', 'class': 'form-control', 'type': 'tel', "id":"phone_number", "name":"phone_number"}),
    )    
    password = forms.CharField(
        max_length=110, 
        widget=forms.TextInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'type': 'password'})
    )
    confirm_password = forms.CharField(
        max_length=110, 
        widget=forms.TextInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'type': 'password'})
    )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control', 'autofocus':True})
        )
    password = forms.CharField(
        max_length=300,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
        )

    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_active:
            raise forms.ValidationError("The account is inactive or not verified", code='inactive')