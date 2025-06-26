from django.urls import path
from . import views

app_name = 'calculos'  # namespace para las URLs

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('calculadora/', views.ir_a_calculadora_streamlit, name='calculadora_streamlit'),
    
    # Secciones académicas
    path('matematica-avanzada/', views.matematica_avanzada, name='matematica_avanzada'),
    path('fisica/', views.fisica, name='fisica'),
    path('quimica/', views.quimica, name='quimica'),
    path('aritmetica/', views.aritmetica, name='aritmetica'),
    path('algebra/', views.algebra, name='algebra'),
    path('geometria/', views.geometria, name='geometria'),
    path('calculo/', views.calculo, name='calculo'),
    path('estadistica/', views.estadistica, name='estadistica'),
    path('topologia/', views.topologia, name='topologia'),
]