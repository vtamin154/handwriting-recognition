import csv
import numpy as np
from hog import Hog

class Recognition:

    def get_sample(self, filename): # lấy vector đặc trưng trong file mẫu
            file = open(filename)
            csvreader = csv.reader(file)
            rows = []
            for row in csvreader:
                rows.append(row)
            file.close()
            return rows
    def euclid_distance(self, letter_features, sample_features):
        distance = np.sqrt(np.sum(np.square(letter_features - sample_features)))
        return distance
    def recognition(self):
        hog = Hog()
        letter_features = hog.extractFeature('resize_img.png')
        result = {}
        samples = self.get_sample('data.csv')
        
        for row in samples:
            sample_features = [float(x) for x in row[1:]]
            distance = self.euclid_distance(letter_features,sample_features)

            result[row[0]] = distance

        result = sorted([(v, k) for (k, v) in result.items()])

        return result[:1]
