from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.shortcuts import resolve_url


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        Female = "F", "여성"



    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
                                 max_length=13,
                                 blank=True)
    gender = models.CharField(choices=GenderChoices.choices, default=GenderChoices.MALE, max_length=1, 
                            blank=True
                            )
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d",
                                help_text="48px * 48px 크기의 png/jpg 파일을 업로드 해주세요")

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)



# class Profile(models.Model):
#     pass
