from shutil import copyfile

import cv2
import imutils as imutils
import numpy as np
from pdf2image import convert_from_path
import PIL
from PIL import Image
from os import listdir
from os.path import isfile, join


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
            if bigger[1] < (img_y - pt[1]) / img_y:
                found = True
                bigger = pt[0] / img_x, (img_y - pt[1]) / img_y

    if found:
        return bigger
    return x, y


def size(img_path):
    image = cv2.imread(img_path)
    image_y, image_x, _ = image.shape
    return image_x, image_y


def pdf2img(input_path, output_path, dpi=500):
    pages = convert_from_path(input_path, dpi)
    for page in pages:
        page.save(output_path, 'JPEG')
        break


def pdf2multiple_img(work_dir, input_path, output_path, dpi=500):
    convert_from_path(input_path, dpi, output_folder=work_dir, fmt="jpg")

    paths = [work_dir + "/" + f for f in listdir(work_dir)
             if isfile(join(work_dir, f))]
    paths.reverse()
    imgs = [PIL.Image.open(i) for i in paths]

    if len(paths) > 1:
        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        # imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
        # imgs_comb = np.hstack((np.asarray(i) for i in imgs))
        # save that beautiful picture
        # imgs_comb = PIL.Image.fromarray(imgs_comb)

        # for a vertical stacking it is simple: use vstack
        # imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = np.vstack((np.asarray(i) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save(output_path)
    else:
        copyfile(paths[0], output_path)
