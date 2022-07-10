"""holofin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return redirect('users:dashboard')
    

urlpatterns = [
    path('', home),
    path('d/admin/', admin.site.urls),
    path('core/', include('apps.core.urls')),
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.users.auth_urls')),
    path('institution/', include('apps.institution.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
