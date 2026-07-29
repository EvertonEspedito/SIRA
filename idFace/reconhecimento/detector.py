import cv2


class Detector:

    def __init__(self):

        self.classificador = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

    def detectar(self, frame):

        cinza = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.classificador.detectMultiScale(
            cinza,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(120, 120)
        )

        return faces, cinza


detector = Detector()


def detectar(frame):

    return detector.detectar(frame)