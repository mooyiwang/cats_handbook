from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}),
                               error_messages={'required': '用户名不能为空', 'min_length': '用户名最少为3个字符',
                                               'max_length': '用户名最不超过为12个字符'}, )
    password = forms.CharField(label="密码", max_length=12,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password1 = forms.CharField(label="密码", max_length=12,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    password2 = forms.CharField(label="确认密码", max_length=12,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))

class CheckcatForm(forms.Form):
    cat = forms.ModelChoiceField(label="打卡猫咪", queryset=Cat.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    addr = forms.ModelChoiceField(label="打卡位置", queryset=Addr.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    time = forms.DateField(label="打卡时间", widget=forms.DateInput(attrs={'class': 'form-control'}))

class FeedForm(forms.Form):
    cat = forms.ModelChoiceField(label="投喂猫咪", queryset=Cat.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    addr = forms.ModelChoiceField(label="投喂位置", queryset=Addr.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    food = forms.ModelChoiceField(label="投喂食品", queryset=Food.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    time = forms.DateField(label="投喂时间", widget=forms.DateInput(attrs={'class': 'form-control'}))
