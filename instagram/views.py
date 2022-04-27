from email import message
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm

from .models import Post, Tag

from django.contrib import messages


@login_required
def post_new(request):
    if request.method =="POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) #commit = False ==> db에 저장하지 않는다
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list()) ##pk가 꼭 필요하므로 post가 생성된 이후에 tag에 넣는다.
            
            messages.success(request, 'post생성 성공')
            return redirect('/') ## TODO:get_absolute_url vies에서 활용해야한다.
    else:
        form = PostForm()

    return render(request,"instagram/post_form.html",{
        'form':form,
    })