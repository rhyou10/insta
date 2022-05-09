from distutils.command.upload import upload
from django.db import models
#from accounts.models import User
from django.conf import settings #user 모델을 불러올때 accounts에서 찾는거 보다 settings에서 불러오는것이 좋다.
import re

from django.urls import reverse

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel ):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='instagram/post/%Y/%m/%d',blank=True)
    caption = models.TextField(max_length=500) #
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})


    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Zㄱ-힣\d]+)", self.caption)## 정규표현식에 (   ) 를 통해 내가 원하는 부분만 가지고올수 있다.
        tag_list = []
        for tag_name in tag_name_list:
            tag,_ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return  tag_list

    def get_absolute_url(self):
        return reverse("instagram:post_detail", args=[self.pk])
    
        

    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name