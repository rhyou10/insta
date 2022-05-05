from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django.views.generic import RedirectView

#import django_pydenticon.urls# 쓰지마
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),
    path('',RedirectView.as_view(pattern_name='instagram:index') ,name='root'),
    path('instagram/',include('instagram.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns+=[
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.MEDIA_URL, 
                document_root = settings.MEDIA_ROOT) 