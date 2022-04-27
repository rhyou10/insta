from tkinter import Widget
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'caption', 'location']
        wdigets= {
            "caption":forms.Textarea, #form에 입력 모양을 변경
        }