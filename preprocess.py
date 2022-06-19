import cv2
from cv2 import resize
import numpy as np


class PreProcess:
    def __init__(self, filename):
        self.filename = filename

    def binaryImage(self):
        img = cv2.imread(self.filename, 2)
        ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite('binary.png', bw_img)

    def cropImg(self):
        img = cv2.imread("binary.png", 2)
        rows, cols = img.shape
        # print("shape", rows, cols)

        def top(image):
            t = 0
            for i in range(rows):
                for j in range(cols):
                    if(image[i][j] == 0):
                        t = i
                        return t

            return t

        def bottom(image):
            b = 0
            t = top(image)
            for i in range(t, rows):
                for j in range(cols):
                    if(image[i][j] == 0):
                        b = i
            return b

        def left(image):
            l = 0
            for i in range(rows):
                for j in range(cols):
                    if(image[j][i] == 0):
                        l = i
                        return l
            return l

        def right(image):
            r = 0
            l = left(image)
            for i in range(rows):
                for j in range(l, cols):
                    if(image[j][i] == 0):
                        r = i
            return r

        t = top(img)
        b = bottom(img)
        l = left(img)
        r = right(img)

        # print(t, b, l, r)

        crop_img = [[0 for i in range(r-l+1)] for j in range(b-t+1)]
        for i in range(b-t+1):
            for j in range(r-l+1):
                crop_img[i][j] = img[i+t][j+l]
        # print(crop_img)
        crop_img = np.reshape(crop_img, (b-t+1, r-l+1))
        cv2.imwrite('crop_img.png', crop_img)

    def resizeImg(self):
        img = cv2.imread('crop_img.png', 2)
        imgResize = resize(img, (32, 32))
        # print(imgResize.shape)
        cv2.imwrite('resize_img.png', imgResize)
