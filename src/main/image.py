from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path


def find(query, universe):
    image = cv2.imread(universe)
    template = cv2.imread(query)
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    argmax = res.argmax()
    shape = res.shape
    x = y = None
    if argmax > 750000:
        y, x = np.unravel_index(res.argmax(), res.shape)
        _, img_y = size(universe)
        y = img_y - y
    return x, y


def size(img_path):
    image = cv2.imread(img_path)
    image_y, image_x, _ = image.shape
    return image_x, image_y


def pdf2img(input_path, output_path):
    pages = convert_from_path(input_path, 500)

    for page in pages:
        page.save(output_path, 'JPEG')
        break
