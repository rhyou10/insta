from email import message
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm

from .models import Post, Tag
from django.contrib.auth import get_user_model
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
            return redirect(post) ## TODO:get_absolute_url vies에서 활용해야한다.
    else:
        form = PostForm()

    return render(request,"instagram/post_form.html",{
        'form':form,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, "instagram/post_detail.html",{
        'post':post,
    }
    )

def user_page(request,username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    return render(request, 'instagram/user_page.html',{
        "page_user" : page_user,
        "post_list" : post_list,
    })
