from django.contrib import admin
from django.urls import path
from core.views import homePage, questionnaire, qr_redirect  # ✅ this line is crucial
from django.urls import path
from . import views

urlpatterns = [
    path("", homePage, name='index'),  # ✅ uses the QR-generating homePage
    path("admin/", admin.site.urls),
    path("questionnaire/<int:questionaire_id>/", questionnaire, name='questionnaire'),
    path("qr/", qr_redirect, name='qr_redirect'),
]

urlpatterns = [
    path('', views.homePage, name='home'),
    path('loading/', views.loading_view, name='loading'),
    path('matches/', views.show_matches, name='show_matches'),
    path('questionnaire/<int:questionaire_id>/', views.questionnaire, name='questionnaire'),
    path('qr/', views.qr_redirect, name='qr_redirect'),
]
