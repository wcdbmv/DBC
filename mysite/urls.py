"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import include, path

from myblog.views.register import RegisterView

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('blog/feed/')),
    path('admin/', admin.site.urls),
    path('blog/', include('myblog.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='myblog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:feed')),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),  # for logout
]
