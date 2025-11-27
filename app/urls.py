from django.urls import path
from . import views

urlpatterns = [
    path('', views.tela_comecar, name='tela_comecar'),
    path('comecar/', views.tela_comecar, name='comecar'),
    path('pergunta/dupla/<int:step>/', views.pergunta_dupla, name='pergunta_dupla'),
    path('pergunta/tripla/<int:step>/', views.pergunta_tripla, name='pergunta_tripla'),
    path('salvar-preferencia/', views.salvar_preferencia, name='salvar_preferencia'),
    path('resultados/', views.resultados, name='resultados'),
    path('pet/<int:pet_id>/', views.pet_detalhes, name='pet_detalhes'),
    path('cadastrar-pet/', views.cadastrar_pet, name='cadastrar_pet'),
    path('painel/pets/', views.painel_pets, name='painel_pets'),
    path('pets/<int:pet_id>/editar/', views.editar_pet, name='editar_pet'),
    path('pets/<int:pet_id>/excluir/', views.excluir_pet, name='excluir_pet'),
    path('pets/<int:pet_id>/alternar-disponibilidade/', views.alternar_disponibilidade_pet, name='alternar_disponibilidade_pet'),
    path('base/', views.tela_base, name='tela_base'),
    path('header/', views.header, name='header'),
    path('footer/', views.footer, name='footer'),
    # Core admin URLs
    path('core/', views.core_login, name='core_login'),
    path('core/login/', views.core_login, name='core_login'),
    path('core/logout/', views.core_logout, name='core_logout'),
    path('core/dashboard/', views.core_dashboard, name='core_dashboard'),
    path('core/cadastrar-pet/', views.core_cadastrar_pet, name='core_cadastrar_pet'),
        path('pets/<int:pet_id>/alternar-disponibilidade/', views.alternar_disponibilidade_pet, name='alternar_disponibilidade_pet'),
]