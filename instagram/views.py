from email import message
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm

from django.db.models import Q
from .models import Post, Tag
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone

from datetime import timedelta

@login_required
def index(request):

    timesince=timezone.now() - timedelta(days=3) #3일 이전의 시간만
    # 팔로윙 한 유저의 게시물만 본다.
    post_list = Post.objects.all()\
                            .filter(
                                Q(author=request.user) |
                                Q(author__in=request.user.following_set.all())
                            )\
                            .filter(
                                created_at__lte=timesince #less than equal
                            )


    suggested_user_list = get_user_model().objects.all()\
                            .exclude(pk=request.user.pk)\
                            .exclude(pk__in=request.user.following_set.all())[:3]
                            
    return render(request, "instagram/index.html",{
        'post_list' : post_list,
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

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post,pk=pk)
    #TODO : like 처리
    post.like_user_set.add(request.user)
    messages.success(request, f"포스팅 {post.pk}를 좋아합니다.")
    redirect_url=request.META.get("HTTP_REFERER", "root") #현재페이지 가지고오기
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post,pk=pk)
    #TODO : unlike 처리
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅 {post.pk}의 좋아요를 취소합니다.")
    redirect_url=request.META.get("HTTP_REFERER", "root") #현재페이지 가지고오기
    return redirect(redirect_url)



def user_page(request,username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)

    

    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists() #로그인시 user, 없을시 annoymoususer
    else:
        is_follow = False

    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() #실제 데이터베이스 count 쿼리를 던지게된다. 이게 더 빠르다.
    #len(post_list) # 이경우 메모리를 많이 사용한다.
    return render(request, 'instagram/user_page.html',{
        "page_user" : page_user,
        "post_list" : post_list,
        "post_list_count" : post_list_count,
        "is_follow":is_follow,
    })
