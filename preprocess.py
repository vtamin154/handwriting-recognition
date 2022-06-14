from operator import le
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

    def thinningImg(self):
        print("thinning")

        def neighbours(x, y, image):
            img = image
            x_1, y_1, x1, y1 = x-1, y-1, x+1, y+1
            return [img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1], img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1]]

        def transitions(neighbours):
            n = neighbours + neighbours[0:1]
            return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

        image = cv2.imread('binary.png', 2)
        r, c = image.shape

        bw_img = [[0]*c]*r
        img_thinning = image.copy()

        for i in range(1, r-1):
            for j in range(1, c - 1):
                if(image[i][j] == 255):
                    bw_img[i][j] = 0
                else:
                    bw_img[i][j] = 1

        changing1 = changing2 = 1

        while changing1 or changing2:
            changing1 = []
            rows, columns = image.shape
            for x in range(1, rows - 1):
                for y in range(1, columns - 1):
                    P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(
                        x, y, bw_img)
                    if(bw_img[x][y] == 1 and 2 <= sum(n) <= 6 and transitions(n) == 1 and P2*P4*P6 == 0 and P4 * P6 * P8 == 0):
                        changing1.append((x, y))
            for x, y in changing1:
                img_thinning[x][y] = 255

            changing2 = []
            for x in range(1, rows - 1):
                for y in range(1, columns - 1):
                    P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(
                        x, y, bw_img)
                    if(bw_img[x][y] == 1 and 2 <= sum(n) <= 6 and transitions(n) == 1 and P2*P4*P8 == 0 and P2*P6*P8):
                        changing2.append((x, y))
                for x, y in changing2:
                    img_thinning[x][y] = 255

        # print(img_thinning[0][0])
        cv2.imwrite('thinning.png', img_thinning)

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

        print(t, b, l, r)

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
        cv2.imwrite('resize_img.png', imgResize)
