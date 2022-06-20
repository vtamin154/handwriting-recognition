from cv2 import imread, imshow
import numpy as np
from scipy import signal
import csv



class Hog:
    # def __init__(self, filename):
    #     self.filename = filename

    def extractFeature(self, filename):
        img = imread(filename, 2)

        def hog(img):
            cell_size = 8 # kích thước cell - pixel
            block_size = 2 # kích thước khối block
            bins = 9 # số chiều vector

            # chuẩn hóa vector
            def normalize(v):
                max_value = max(v)
                min_value = min(v)
                return np.array([2*(v[i] - min_value)/(max_value - min_value) - 1 for i in range (len(v))])

            # nếu direction thuộc vào khoảng [160, 180)
            def assign_bucket_vals(m, d, bucket_vals):
                if not np.isnan(d):
                    if d >= 160:
                        left_bin = bins - 1  
                        right_bin = 0
                        left_val = m * (bins * 20 - d)/ 20
                    else:
                        left_bin = int(d/20.)
                        right_bin = (int(d/20.) + 1) % bins
                        left_val = m * (right_bin * 20 - d)/20
                    right_val = m * (d - left_bin*20)/20

                    bucket_vals[left_bin] += left_val
                    bucket_vals[right_bin] += right_val

            height, width = img.shape

            xkernel = np.array([[-1, 0, 1]])
            ykernel = np.array([[-1], [0], [1]])

            # đạo hàm ảnh = nhân tích chập ảnh với nhân (mặt nạ đạo hàm)
            dx = signal.convolve2d(img, xkernel, mode='same')
            dy = signal.convolve2d(img, ykernel, mode='same')

            # độ lớn gradient
            magnitude = np.sqrt(np.square(dx) +  np.square(dy))

            # hướng gradient
            orientation = np.arctan(np.divide(dy, dx + 0.00001))
            orientation = np.degrees(orientation) # [-90; 90]
            orientation += 90 # [0; 180]
            
            # normalization - chuẩn hóa
            # tính số cell theo trục x và y
            num_cell_x = width // cell_size # 
            num_cell_y = height // cell_size 

            # print("num cell x", num_cell_x, num_cell_y)

            histogram = np.zeros([num_cell_y, num_cell_x, bins])
            for x in range(num_cell_x):
                for y in range(num_cell_y):
                    direct = orientation[y*cell_size:y*cell_size + cell_size, x*cell_size:x*cell_size + cell_size]
                    magn = magnitude[y*cell_size:y*cell_size+cell_size, x*cell_size:x*cell_size+cell_size]

                    bucket_vals = np.zeros(bins)


                    for (m, d) in zip(magn.flatten(), direct.flatten()):
                        assign_bucket_vals(m,d,bucket_vals)

                    # print("bucket", bucket_vals)
                    histogram[y, x, :] = bucket_vals

            redundant_cell = block_size-1
            features = np.zeros([num_cell_y - redundant_cell, num_cell_x - redundant_cell, block_size*block_size*bins])

            for x in range (num_cell_x - redundant_cell):
                for y in range (num_cell_y - redundant_cell):
                    start_x = x
                    end_x = x + block_size

                    start_y = y
                    end_y = y + block_size

                    v=histogram[start_y:end_y, start_x:end_x, :].flatten()

                    features[y, x, :] = v/np.linalg.norm(v)

                    if np.isnan(features[y, x, :]).any():
                        features[y, x :] = v
            print(features.flatten())
            return normalize(features.flatten())
        features = hog(img)
        return features

                    
        