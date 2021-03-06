"""rest_users_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse

def reload_settings_module(request):
    reload(settings)
    print (settings.EMAIL_PORT)
    return HttpResponse(settings.EMAIL_PORT)


urlpatterns = [
    url(r'^templates/login$', TemplateView.as_view(template_name="login.html")),
    url(r'^templates/signup$', TemplateView.as_view(template_name="signup.html")),
    url(r'^templates/landing$', TemplateView.as_view(template_name="landing.html")),
    url(r'^templates/activation-failed$', TemplateView.as_view(template_name="activation-failed.html")),
    url(r'^templates/activation-success$', TemplateView.as_view(template_name="activation-success.html")),
    url(r'^templates/change-password$', TemplateView.as_view(template_name="change-password.html")),
    url(r'^templates/accept-email$', TemplateView.as_view(template_name="accept-email.html")),
    url(r'^templates/reset-password$', TemplateView.as_view(template_name="reset-password.html")),
    url(r'^templates/reset-success$', TemplateView.as_view(template_name="reset-success.html")),
    url(r'^templates/reset-failed$', TemplateView.as_view(template_name="reset-failed.html")),
    url("reload", reload_settings_module),
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    
    url(r'^users/', include("rest_users.urls")),
]
