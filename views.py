from django.shortcuts import render, redirect
from .models import Articulo, Cita, Estado, Estudio, Habilidad, Musica, Proyecto, Usuario, Videos, ProyectoHabilidad, Componente
from xhtml2pdf import pisa
from django.views import View
from django.template.loader import get_template
from django.http import HttpResponse
from datetime import date
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
import requests
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from weasyprint import HTML



load_dotenv()

#generar curriculum pdf ingles
class GeneratePDF_EN(View):
    def get(self, request, *args, **kwargs):
        fecha_actual = date.today().strftime("%m/%d/%Y")
        citas = Cita.objects.all().order_by('?')
        cita= citas.first()
        proyectos = Proyecto.objects.all()
        articulos = Articulo.objects.all().order_by('fecha')
        estudios = Estudio.objects.all().order_by('-fecha')
        estados = Estado.objects.all()
        videos = Videos.objects.all()
        diccionario_proyectos = list()
        habilidadesGeneral = list()
        for p in proyectos:
            habilidades = list()
            habilidadesProyecto = ProyectoHabilidad.objects.filter(proyecto=p)
            componentesProyecto = Componente.objects.filter(proyecto=p)
            for h in habilidadesProyecto:
                habilidades.append(h.habilidad.nombre)
                habilidadesGeneral.append(h.habilidad.nombre)
            habilidades.sort()
            dic = {'proyecto':p, 'habilidades':habilidades, 'componentes':componentesProyecto}
            diccionario_proyectos.append(dic)
        habilidadesGeneral = list(set(habilidadesGeneral))
     
        template = get_template('portafolio_app/pdf_template_en.html')  # Reemplaza 'pdf_template.html' con tu propio template HTML
        context = {
            'proyectos':diccionario_proyectos,
            'cita': cita,
            'articulos':articulos,
            'estudios':estudios,
            'habilidades':habilidades,
            'estados':estados,
            'videos':videos,
            'habilidadesGeneral':habilidadesGeneral,
            'fecha_actual':fecha_actual
        }  

        html = template.render(context)
        pdf = HTML(string=html).write_pdf()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="curriculum_nicolas_valdes.pdf"'
        response.write(pdf)
        return response

#generar curriculum pdf español
class GeneratePDF_ES(View):
    def get(self, request, *args, **kwargs):
        fecha_actual = date.today().strftime("%d/%m/%Y")
        citas = Cita.objects.all().order_by('?')
        cita= citas.first()
        proyectos = Proyecto.objects.all()
        articulos = Articulo.objects.all().order_by('fecha')
        estudios = Estudio.objects.all().order_by('-fecha')
        estados = Estado.objects.all()
        videos = Videos.objects.all()
        diccionario_proyectos = list()
        habilidadesGeneral = list()
        for p in proyectos:
            habilidades = list()
            habilidadesProyecto = ProyectoHabilidad.objects.filter(proyecto=p)
            componentesProyecto = Componente.objects.filter(proyecto=p)
            for h in habilidadesProyecto:
                habilidades.append(h.habilidad.nombre)
                habilidadesGeneral.append(h.habilidad.nombre)
            habilidades.sort()
            dic = {'proyecto':p, 'habilidades':habilidades, 'componentes':componentesProyecto}
            diccionario_proyectos.append(dic)
        habilidadesGeneral = list(set(habilidadesGeneral))
     
        template = get_template('portafolio_app/pdf_template_es.html')  # Reemplaza 'pdf_template.html' con tu propio template HTML
        context = {
            'proyectos':diccionario_proyectos,
            'cita': cita,
            'articulos':articulos,
            'estudios':estudios,
            'habilidades':habilidades,
            'estados':estados,
            'videos':videos,
            'habilidadesGeneral':habilidadesGeneral,
            'fecha_actual':fecha_actual
        }  

        html = template.render(context)
        pdf = HTML(string=html).write_pdf()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="curriculum_nicolas_valdes.pdf"'
        response.write(pdf)
        return response

# Create your views here.
def index(request):
    citas = Cita.objects.all().order_by('?')
    cita= citas.first()
    proyectos = Proyecto.objects.all()
    articulos = Articulo.objects.all().order_by('fecha')
    estudios = Estudio.objects.all().order_by('-fecha')
    habilidades = Habilidad.objects.all()
    estados = Estado.objects.all()
    videos = Videos.objects.all()
    diccionario_proyectos = list()
    posts = list()

    for p in proyectos:
        habilidades = list()
        habilidadesProyecto = ProyectoHabilidad.objects.filter(proyecto=p)
        componentesProyecto = Componente.objects.filter(proyecto=p)
        for h in habilidadesProyecto:
            #habilidades.append(h.habilidad.nombre)
            #saqui agregar el icono 
            habilidades_detalle = (h.habilidad.nombre, h.habilidad.icon_path )
            habilidades.append(habilidades_detalle)
        habilidades.sort()
        dic = {'proyecto':p, 'habilidades':habilidades, 'componentes':componentesProyecto}
        diccionario_proyectos.append(dic)

    for v in videos:
        tupla = (v.nombre, v.url, v.fecha, 'video')
        posts.append(tupla)
    for a in articulos:
        tupla = (a.titulo, a.recurso, a.fecha, 'articulo')
        posts.append(tupla)
    # Ordena la lista posts por la fecha, que es el tercer elemento de cada tupla
    posts_ordenados = sorted(posts, key=lambda x: x[2], reverse=True)
    #obtener la lista de habilidades que tengan porcentaje de mayor a cero 
    progreso_habilidades = Habilidad.objects.filter(progreso__gt=0).order_by('-progreso')
     
    context = {
        'proyectos':diccionario_proyectos,
        'cita': cita,
        'articulos':articulos,
        'estudios':estudios,
        'habilidades':habilidades,
        'estados':estados,
        'videos':videos,
        'posts': posts_ordenados,
        'error':True,
        'progreso_habilidades':progreso_habilidades
    }

    return render(request, 'portafolio_app/index.html', context)

#creacion del correo
def send_email(name,mail,message):
    email = EmailMessage(
        subject='contacto desde portafolio',
        body=f'un mensaje fue enviado de  {name} desde nicolasvaldes.dev , mensaje : {message}',
        from_email='nicolas.valdeslobos@gmail.com',
        to=[mail],
    )   
    email.send()

#vista para enviar correo
def enviar_correo(request):
    if request.method == 'POST':
        captcha_response = request.POST.get('g-recaptcha-response', '')
        captcha_data = {
            'secret': os.getenv("SECRET_KEY_CAPTCHA"),
            'response': captcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
        result = response.json()
        if result['success']:
            name = request.POST.get('demo-name', '')
            email = request.POST.get('demo-email', '')
            message = request.POST.get('demo-message', '')
            send_email(name,'nicolas.valdes@live.com',message)
            if(email != ''):
                send_email(name,email,message)
    return redirect('index')


def error_404(request, exception):
    return render(request, 'portafolio_app/error2.html', status=404)

def error_500(request):
    return render(request, 'portafolio_app/error2.html', status=500)