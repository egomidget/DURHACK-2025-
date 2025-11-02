"""
URL configuration for durhack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from core.views import homePage, questionnaire, qr_redirect
from django.urls import path
from . import views
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", homePage, name="index"),
    path("admin/", admin.site.urls),
    path("questionnaire/<int:questionaire_id>/", questionnaire, name="questionnaire"),
    path("qr/", qr_redirect, name="qr_redirect"),
    path("see_match/", see_match, name='see_match'),
    path("process/", process_matches, name='process_matches')
]

urlpatterns = [
    path('matches/', views.show_matches, name='show_matches'),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  
]
