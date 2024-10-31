# portafolio_app/urls.py
from django.urls import path
from .views import index
from django.conf.urls.static import static
from django.conf import settings
from .views import GeneratePDF_EN, GeneratePDF_ES, enviar_correo

urlpatterns = [
    path('', index, name='index'),
    path('generate_pdf_en/', GeneratePDF_EN.as_view(), name='generate_pdf_en'),
    path('generate_pdf_es/', GeneratePDF_ES.as_view(), name='generate_pdf_es'),
    path('enviar_correo/', enviar_correo, name='enviar_correo'),
]
