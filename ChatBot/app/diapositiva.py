from pptx import Presentation
from PIL import Image
import io

def convertir_presentacion_a_imagenes(ruta_presentacion):
    presentacion = Presentation(ruta_presentacion)
    imagenes = []
    for i, diapositiva in enumerate(presentacion.slides):
        imagen = io.BytesIO()
        diapositiva_imagen = Image.new("RGB", (800, 600), (255, 255, 255))
        diapositiva._write_png(imagen)
        imagenes.append(imagen.getvalue())
    return imagenes