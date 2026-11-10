from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('pokemon/', views.pokemon, name='pokemon'),
    path('pokemon/<int:pokemon_id>/', views.pokemon_detalle, name='pokemon_detalle'),

    path('entrenador/', views.entrenadores, name='entrenadores'),
    path('entrenador/<int:entrenador_id>/', views.entrenador_detalle, name='entrenador_detalle'),
    path('registrar_entrenador/', views.registrar_entrenador, name='registrar_entrenador'),
    path('editar_entrenador/<int:entrenador_id>/',views.editar_entrenador,name='editar_entrenador'),
    path('eliminar_entrenador/<int:entrenador_id>/',views.eliminar_entrenador,name='eliminar_entrenador'),

    path('gimnasios/', views.gimnasios, name='gimnasios'),
    path('agregar_gimnasio/',views.agregar_gimnasio,name='agregar_gimnasio'),
    path('detalle_gimnasio/<int:gimnasio_id>/',views.detalle_gimnasio,name='detalle_gimnasio'),
    path('editar_gimnasio/<int:gimnasio_id>/',views.editar_gimnasio,name='editar_gimnasio'),
    path('eliminar_gimnasio/<int:gimnasio_id>/',views.eliminar_gimnasio,name='eliminar_gimnasio'),
    path('probar-api/', views.probar_api, name='probar_api'),

]
