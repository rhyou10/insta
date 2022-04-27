import email
from .models import User
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
)
from django import forms

class SignupForm(UserCreationForm):
    # class Meta:
    #     model = User
    #     fields= ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


    class Meta(UserCreationForm.Meta):
        model = User # User를 변경하였기때문에 지정해줘야한다.
        fields = ['username', 'email', 'first_name', 'last_name']
    

    def clean_email(self): ## 이메일 중복 방지
        email = self.cleaned_data.get('email') 
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email
    

class ProfileFrom(forms.ModelForm):
    class Meta:
        model= User
        fields = ['avatar', 'first_name', 'last_name', 'website_url', 'bio', 'phone_number', 'gender']


class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        new_password2 = super().clean_new_password2()
        if old_password == new_password2:
            raise forms.ValidationError('새로운 암호와 기존암호가 일치합니다.')
        else:
            return new_password2