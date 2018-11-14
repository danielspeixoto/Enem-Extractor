import cv2
import numpy as np
from pdf2image import convert_from_path


def find(query, universe):
    image = cv2.imread(universe)
    template = cv2.imread(query)
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    x = y = None
    _, confidence, _, coordinates = cv2.minMaxLoc(res)
    threshold = 0.6

    loc = np.where(res >= max(threshold, confidence - 0.1))
    bigger = (10000, 10000)
    for pt in zip(*loc[::-1]):
        if bigger[1] > pt[1]:
            bigger = pt

    if confidence > threshold:
        x, y = bigger[0], bigger[1]
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
