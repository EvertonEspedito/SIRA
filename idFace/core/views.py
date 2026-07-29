import json
import base64

import cv2
import numpy as np
from deepface import DeepFace

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Pessoa, Presenca
from reconhecimento.servico import ServicoReconhecimento

def gerar_embedding(pessoa):

    if not pessoa.foto:
        return

    resultado = DeepFace.represent(
        img_path=pessoa.foto.path,
        model_name="Facenet",
        enforce_detection=False
    )

    print("Embedding cadastro:", len(resultado[0]["embedding"]))

    pessoa.embedding = resultado[0]["embedding"]
    pessoa.save()


def login(request):

    if request.method == "POST":

        usuario = request.POST.get("username")
        senha = request.POST.get("password")

        user = authenticate(
            request,
            username=usuario,
            password=senha
        )

        if user:
            auth_login(request, user)
            return redirect("dashboard")

        messages.error(
            request,
            "Usuário ou senha inválidos."
        )

    return render(request, "login.html")


def sair(request):

    logout(request)

    return redirect("login")




@login_required(login_url="login")
def dashboard(request):

    hoje = timezone.now().date()

    total_pessoas = Pessoa.objects.count()

    total_presencas = Presenca.objects.filter(
        data_hora__date=hoje
    ).count()

    ultimas_presencas = (
        Presenca.objects
        .select_related("pessoa")
        .order_by("-data_hora")[:10]
    )

    contexto = {
        "totalPessoas": total_pessoas,
        "totalHoje": total_presencas,
        "ultimasPresencas": ultimas_presencas,
    }

    return render(
        request,
        "dashboard.html",
        contexto
    )

@login_required(login_url="login")
def cadastro_aluno(request):

    if request.method == "POST":

        try:

            foto = request.FILES.get("foto")

            if not foto:

                messages.error(
                    request,
                    "Selecione uma foto do aluno."
                )

                return redirect("cadastro_aluno")

            aluno = Pessoa.objects.create(

                nome=request.POST.get("nome"),
                matricula=request.POST.get("matricula"),
                email=request.POST.get("email"),
                tipo="ALUNO",
                foto=foto

            )

            gerar_embedding(aluno)

            messages.success(
                request,
                "Aluno cadastrado com sucesso."
            )

            return redirect("dashboard")

        except Exception as erro:

            messages.error(
                request,
                f"Erro ao cadastrar aluno: {erro}"
            )

    return render(
        request,
        "cadastro_aluno.html"
    )

@login_required(login_url="login")
def cadastro_visitante(request):

    if request.method == "POST":

        try:

            foto = request.FILES.get("foto")

            if not foto:

                messages.error(
                    request,
                    "Selecione uma foto do visitante."
                )

                return redirect("cadastro_visitante")

            visitante = Pessoa.objects.create(

                nome=request.POST.get("nome"),
                cpf=request.POST.get("cpf"),
                motivo_visita=request.POST.get("motivo"),
                tipo="VISITANTE",
                foto=foto

            )

            gerar_embedding(visitante)

            messages.success(
                request,
                "Visitante cadastrado com sucesso."
            )

            return redirect("dashboard")

        except Exception as erro:

            messages.error(
                request,
                f"Erro ao cadastrar visitante: {erro}"
            )

    return render(
        request,
        "cadastro_visitante.html"
    )


@login_required(login_url="login")
def cadastro_about(request):

    return render(
        request,
        "cadastro_about.html"
    )


@login_required(login_url="login")
def sobre_nos(request):

    return render(
        request,
        "sobre_nos.html"
    )


@login_required(login_url="login")
def reconhecimento(request):

    return render(
        request,
        "reconhecimento.html"
    )


@login_required(login_url="login")
def reconhecer(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "erro": "Método inválido."
            },
            status=405
        )

    try:

        dados = json.loads(request.body)

        imagem = dados.get("imagem")

        if not imagem:

            return JsonResponse(
                {
                    "erro": "Imagem não enviada."
                },
                status=400
            )

        if "," in imagem:

            imagem = imagem.split(",")[1]

        imagem = base64.b64decode(imagem)

        imagem = np.frombuffer(
            imagem,
            np.uint8
        )

        frame = cv2.imdecode(
            imagem,
            cv2.IMREAD_COLOR
        )

        servico = ServicoReconhecimento()

        pessoa, confianca = servico.reconhecer(frame)

        if pessoa is None:

            return JsonResponse({

                "status": "NAO_ENCONTRADO",

                "nome": "",

                "tipo": "",

                "confianca": 0

            })

        return JsonResponse({

            "status": "SUCESSO",

            "nome": pessoa.nome,

            "tipo": pessoa.tipo,

            "confianca": round(float(confianca), 4)

        })

    except Exception as erro:

        return JsonResponse(
            {
                "erro": str(erro)
            },
            status=500
        )


    