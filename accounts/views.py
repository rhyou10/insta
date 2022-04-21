from tokenize import Single
from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib import messages

def signup(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "회원가입 성공")
            return redirect("root")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html',{
        'form':form,
    })
