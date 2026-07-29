import numpy as np

from core.models import Pessoa


# Limiar para reconhecimento
LIMIAR = 1.0


def comparar(embedding):

    embedding = np.array(embedding)

    melhor_pessoa = None
    menor_distancia = float("inf")

    pessoas = (
        Pessoa.objects
        .filter(ativo=True)
        .exclude(embedding=None)
    )

    if not pessoas.exists():
        print("Nenhuma pessoa cadastrada.")
        return None, None

    print("\n========== INICIANDO COMPARAÇÃO ==========")

    for pessoa in pessoas:

        try:

            embedding_pessoa = np.array(pessoa.embedding)

            if embedding.shape != embedding_pessoa.shape:

                print(
                    f"{pessoa.nome}: embeddings incompatíveis "
                    f"{embedding.shape} x {embedding_pessoa.shape}"
                )

                continue

            distancia = np.linalg.norm(
                embedding - embedding_pessoa
            )

            print(
                f"{pessoa.nome} -> Distância: {distancia:.4f}"
            )

            if distancia < menor_distancia:

                menor_distancia = distancia
                melhor_pessoa = pessoa

        except Exception as erro:

            print(
                f"Erro ao comparar {pessoa.nome}: {erro}"
            )

    print("----------------------------------")

    if melhor_pessoa:

        print(f"Melhor pessoa: {melhor_pessoa.nome}")
        print(f"Menor distância: {menor_distancia:.4f}")
        print(f"Limiar: {LIMIAR}")

        if menor_distancia <= LIMIAR:

            print(">>> PESSOA RECONHECIDA <<<\n")

            return melhor_pessoa, menor_distancia

    print(">>> PESSOA NÃO RECONHECIDA <<<\n")

    return None, None