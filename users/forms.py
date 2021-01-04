from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ProfilePic


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['address','number']


class ProfilePicUpdateForm(forms.ModelForm):

    class Meta:
        model = ProfilePic
        fields = ['image']