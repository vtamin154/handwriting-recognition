import argparse
import csv
import os
import random

import cv2
import numpy as np
from hog import Hog

class Recognition:

    def get_sample(self, filename):
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





        



# from search import Search

# ap = argparse.ArgumentParser()

# file_dataset = "hog.csv"
# result_path = "dataset_letter"

# ap.add_argument("-q", "--query", required=True, help="Path to the query image")

# ap.add_argument("-r", "--hog", required=True, help="Path to the result path")

# args = vars(ap.parse_args())
# hog_feature = Hog()
# files = os.listdir(args["query"])
# sample = random.sample(files, 1)

# for s in sample:
#     query_path = args["query"] + '/' + s
#     query = cv2.imread(query_path)

#     cv2.imshow("Query", query)
#     cv2.waitKey(1000)

#     if args["hog"] == 'hog':
#         feature = hog_feature.extractFeature(query_path)

#     search = Search(file_dataset)
#     results = search.search(feature, 1)
#     for(score, resultID) in results:
#         result = cv2.imread(result_path + '/' + resultID)
#     cv2.imshow("Result", result)
#     cv2.waitKey(1000)