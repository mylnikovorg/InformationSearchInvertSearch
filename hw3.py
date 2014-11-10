from functools import reduce
from ipaddress import collapse_addresses
import collections
import math


__author__ = 'alex'

import sys

num = int(sys.stdin.readline())

scores = list()
for score in sys.stdin.readline().split():
    scores.append(score)

# print(scores)


def dcg(n, scores):
    res = 0
    for counter in range(1, len(scores) + 1):
        res += (2 ** int(scores[counter - 1]) - 1) / math.log2(counter + 1)
    return res
    # return reduce(lambda x, y: x + y, scores, 0)


def pfound(n, scores):
    # print(scores)
    res = 0
    look = list()
    look.append(1)
    for count in range(1, n):
        look.append(look[count - 1] * (1 - 0.15) * (1 - scores[count-1]))


    for count in range(len(scores)):
        res+=scores[count]*look[count]
    return res


print("DCG = {}".format(dcg(num, scores)))
# print(list(reversed(sorted(scores))))
# print(dcg(num, list(reversed(sorted(scores)))))

print("NDCG = {}".format(dcg(num, scores) / dcg(num, list(reversed(sorted(scores))))))
t = max(scores)

print("PFound = {}".format(pfound(num, list(map(lambda x: float(x) / float(t), scores)))))



