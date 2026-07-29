import numpy as np
from deepface import DeepFace

from .detector import detectar
from .comparador import comparar
from .registro import registrar


class ServicoReconhecimento:

    def reconhecer(self, frame):

        try:

            faces, _ = detectar(frame)

            if len(faces) == 0:
                print("Nenhum rosto encontrado.")
                return None, None

            # Usa o maior rosto encontrado
            x, y, w, h = max(
                faces,
                key=lambda face: face[2] * face[3]
            )

            rosto = frame[y:y+h, x:x+w]

            if rosto.size == 0:
                print("Recorte do rosto inválido.")
                return None, None

            resultado = DeepFace.represent(
                img_path=rosto,
                model_name="Facenet",
                detector_backend="skip",
                enforce_detection=False
            )

            embedding = np.array(resultado[0]["embedding"])

            pessoa, confianca = comparar(embedding)

            if pessoa:
                registrar(pessoa, confianca)
                return pessoa, confianca

            return None, None

        except Exception as erro:

            print(f"Erro no reconhecimento: {erro}")

            return None, None