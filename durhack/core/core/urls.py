from django.contrib import admin
from django.urls import path
from core.views import homePage, questionnaire, qr_redirect  # ✅ this line is crucial

urlpatterns = [
    path("", homePage, name='index'),  # ✅ uses the QR-generating homePage
    path("admin/", admin.site.urls),
    path("questionnaire/<int:questionaire_id>/", questionnaire, name='questionnaire'),
    path("qr/", qr_redirect, name='qr_redirect'),
]
