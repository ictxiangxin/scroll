__author__ = 'ict'

from calculate.cluster.kmeans import *

data = {
    1: [1, 1],
    2: [1, 2],
    3: [2, 1],
    4: [2, 2],
    5: [1, 4],
    6: [1, 5],
    7: [2, 4],
    8: [2, 5],
    9: [4, 1],
    10: [5, 1],
    11: [4, 2],
    12: [5, 2],
    13: [4, 4],
    14: [4, 5],
    15: [5, 4],
    16: [5, 5],
}

print("kmeans: ", kmeans(data, 4))
print("bikmeans: ", bikmeans(data, 4))