from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path


def find(query, universe):
    image = cv2.imread(universe)
    template = cv2.imread(query)
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    match_indices = np.arange(result.size)[(result > 0.9).flatten()]
    # return np.unravel_index(match_indices, result.shape)
    y, x = np.unravel_index(result.argmax(), result.shape)
    _, img_y = size(universe)
    return [(x, img_y - y)]


def size(img_path):
    image = cv2.imread(img_path)
    image_y, image_x, _ = image.shape
    return image_x, image_y


def pdf2img(input_path, output_path):
    pages = convert_from_path(input_path, 500)

    for page in pages:
        page.save(output_path, 'JPEG')
