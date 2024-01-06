import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO


def imageToBase64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    return base64.b64encode(buffered.getvalue()).decode()


def base64ToImage(base64Image):
    image = Image.open(BytesIO(base64.b64decode(base64Image)))
    image = np.array(image)
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
