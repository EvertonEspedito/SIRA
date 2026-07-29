from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.login,
        name="login"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "logout/",
        views.sair,
        name="logout"
    ),

    path(
        "cadastro/aluno/",
        views.cadastro_aluno,
        name="cadastro_aluno"
    ),

    path(
        "cadastro/visitante/",
        views.cadastro_visitante,
        name="cadastro_visitante"
    ),

    path(
        "cadastro/about/",
        views.cadastro_about,
        name="cadastro_about"
    ),

    path(
        "sobre/",
        views.sobre_nos,
        name="sobre_nos"
    ),

   

    path(
        "reconhecimento/",
        views.reconhecimento,
        name="reconhecimento"
    ),

    path(
        "api/reconhecer/",
        views.reconhecer,
        name="reconhecer"
    ),

]