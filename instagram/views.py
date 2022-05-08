from email import message
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm

from .models import Post, Tag
from django.contrib.auth import get_user_model
from django.contrib import messages

@login_required
def index(request):
    suggested_user_list = get_user_model().objects.all()\
                            .exclude(pk=request.user.pk)\
                            .exclude(pk__in=request.user.following_set.all())[:3]
    return render(request, "instagram/index.html",{
        'suggested_user_list' : suggested_user_list
        
    })

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
    post_list_count = post_list.count() #실제 데이터베이스 count 쿼리를 던지게된다. 이게 더 빠르다.
    #len(post_list) # 이경우 메모리를 많이 사용한다.
    return render(request, 'instagram/user_page.html',{
        "page_user" : page_user,
        "post_list" : post_list,
        "post_list_count" : post_list_count,
    })
