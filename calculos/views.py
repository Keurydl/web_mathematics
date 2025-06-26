from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def pagina_principal(request):
    # Esta es una página simple de Django.
    # Podrías tener aquí un enlace a tu app Streamlit.
    # La app Streamlit se ejecutará en, por ejemplo, http://localhost:8501
    streamlit_url = "http://localhost:8501" # Puerto por defecto de Streamlit
    return render(request, 'calculos/pagina_principal.html', {'streamlit_url': streamlit_url})

from django.shortcuts import redirect

def ir_a_calculadora_streamlit(request):
    # Redirigir directamente a la aplicación Streamlit
    return redirect('http://localhost:8501')

# Vistas para las secciones académicas
def matematica_avanzada(request):
    return render(request, 'calculos/secciones/matematica_avanzada.html', {'titulo': 'Matemática Avanzada'})

def fisica(request):
    return render(request, 'calculos/secciones/fisica.html', {'titulo': 'Física'})

def quimica(request):
    return render(request, 'calculos/secciones/quimica.html', {'titulo': 'Química'})

def aritmetica(request):
    return render(request, 'calculos/secciones/aritmetica.html', {'titulo': 'Aritmética'})

def algebra(request):
    return render(request, 'calculos/secciones/algebra.html', {'titulo': 'Álgebra'})

def geometria(request):
    return render(request, 'calculos/secciones/geometria.html', {'titulo': 'Geometría'})

def calculo(request):
    return render(request, 'calculos/secciones/calculo.html', {'titulo': 'Cálculo'})

def estadistica(request):
    return render(request, 'calculos/secciones/estadistica.html', {'titulo': 'Estadística'})

def topologia(request):
    return render(request, 'calculos/secciones/topologia.html', {'titulo': 'Topología'})