from django import forms
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from accounts.models import userDetails 

class userForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class userProfileForm(forms.ModelForm):
    class Meta:
        model = userDetails 
        fields = ['phone','house_no','street','city','state','zipcode','profile_pic']
    captcha = ReCaptchaField()

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class userDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = userDetails
        fields = ['phone','house_no','street','city','state','zipcode','profile_pic'] 



