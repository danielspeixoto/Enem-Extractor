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
    threshold = 0.7
    found = False
    for scale in [0.8, 0.9, 1]:
        resized = imutils.resize(image, width=int(image.shape[1] * scale))
        if resized.shape[0] >= template.shape[0]:
            res = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
        else:
            return None, None
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


def pdf2multiple_img(work_dir, input_path, output_path):
    dpi = 250
    convert_from_path(input_path, 1000, output_folder=work_dir, fmt="jpg")

    paths = [work_dir + "/" + f for f in listdir(work_dir)
             if isfile(join(work_dir, f))]
    paths.reverse()
    imgs = [PIL.Image.open(i) for i in paths]
    imgs.reverse()

    processed = []
    for RGBimg in imgs:
        HSVimg = RGBimg.convert('HSV')

        # Make numpy versions
        RGBna = np.array(RGBimg)
        HSVna = np.array(HSVimg)

        # Extract Hue
        H = HSVna[:, :, 0]

        # Find all green pixels, i.e. where 100 < Hue < 140
        lo, hi = 100, 140
        # Rescale to 0-255, rather than 0-360 because we are using uint8
        lo = int((lo * 255) / 360)
        hi = int((hi * 255) / 360)
        green = np.where((H > lo) & (H < hi))

        # Make all green pixels white in original image
        RGBna[green] = [255, 255, 255]
        processed.append(PIL.Image.fromarray(RGBna))

    imgs_comb = np.vstack((np.asarray(i)for i in processed))
    imgs_comb = PIL.Image.fromarray(imgs_comb)
    highres_img = work_dir + "highres.jpg"
    imgs_comb.save(highres_img)

    img = cv2.imread(highres_img, cv2.IMREAD_UNCHANGED)
    scale = dpi / 1000
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, resized)

    # img = PythonMagick.Image()
    # img.density("600")
    # img.read(highres_img)
    # img.write(output_path)