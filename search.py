import numpy as np
import csv

class Search:
    def __init__(self, path):
        self.path = path

    def search(self, query_feature, limit=4):
        results = {}

        with open(self.path) as file:
            reader = csv.reader(file)

            for row in reader:
                features = [float(x) for x in row[1:]]
                d = self.distance(features, query_feature)
                results[row[0]] = d
            file.close()
        results = sorted([v, k] for (k, v) in results.items())
        return results[:limit]
    
    def distance(self, a, b, e = 1e-10):
        dist = 0.5*np.sum([((x-y) ** 2)/(x + y + e) for (x,y) in zip(a,b)])
        return dist
    
    