import cv2
import imutils as imutils
import numpy as np
from pdf2image import convert_from_path


def find(query, universe):
    image = cv2.imread(universe)
    template = cv2.imread(query)
    x = y = None
    bigger = (0, 0)
    threshold = 0.6
    found = False
    for scale in [0.8, 0.9, 1]:
        resized = imutils.resize(image, width=int(image.shape[1] * scale))
        if resized.shape[0] >= template.shape[0]:
            res = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
        else:
            return x, y
        loc = np.where(res >= threshold)
        img_x, img_y = size(universe)
        points = zip(*loc[::-1])
        for pt in points:
            if bigger[1] < (img_y - pt[1])/img_y:
                found = True
                bigger = pt[0]/img_x, (img_y - pt[1])/img_y

    if found:
        return bigger
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
