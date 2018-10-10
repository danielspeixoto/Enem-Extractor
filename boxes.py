import cv2


def contour(img_path, output_path):
    image = cv2.imread(img_path)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    tt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # grayscale
    _, tt = cv2.threshold(tt, 50, 255, cv2.THRESH_BINARY_INV) # threshold
    # tt = cv2.erode(tt, kernel, iterations=1)
    # tt = cv2.dilate(tt, kernel, iterations=20) # dilate
    _, contours, hierarchy = cv2.findContours(tt,
                                              cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE) # get contours

    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        # if x > 100:
        #     continue

        # discard areas that are too large
        # if h > 150:
        #     continue

        # #
        # if h < 10 or h > 50 or w > 50:
        #     continue
        #
        if h < 10 or h > 50 or w < 10 or w > 50:
            continue

        # discard areas that are too small
        # if w < 1600 or h < 100:
        #     continue


        # draw rectangle around contour on original image
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),50)

    # write original image with added contours to disk
    cv2.imwrite(output_path, image)


contour("data/1.jpg", "data/contoured.jpg")
