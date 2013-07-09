""" KMeansPP

    K-Means++ clustering algorithm for RGB color.
    RGB color is tuple and each color element takes [0, 255].
        => (R, G, B)
        => (0, 127, 255)
"""

import copy
import math
import random
import sys

class KMeansPP(object):
    """ K-Means++ clustering algorithm class """

    def __init__(self, datas):
        self.__justbefore = []
        self.__assign = []
        self.__results = []
        self.__k = 0
        self.__datas = datas
        self.assign = []
        self.results = []

    def __initialization(self):
        __has_list = []
        __has_list.append(random.randint(0, len(self.__datas)-1))
        __MAX_DIST = 442 #math.sqrt((255-0)**2 + (255-0)**2 + (255-0)**2) < 442
        for ki in range(1, self.__k):
            __popped = __has_list.pop(0)
            __dists = []
            __dist_max = 0
            for di, d in enumerate(self.__datas):
                __ = math.sqrt(
                        (d[0] - self.__datas[__popped][0])**2 +
                        (d[1] - self.__datas[__popped][1])**2 +
                        (d[2] - self.__datas[__popped][2])**2)
                __dists.append((__, di))
            _new_dists = sorted(__dists, key=lambda x:int(x[0]), reverse=True)
            __new_dists = [x for x in _new_dists if x[0] < __MAX_DIST/3]
            for n in __new_dists:
                if n[1] not in __has_list:
                    __has_list.insert(0, n[1])
                    break
            __has_list.append(__popped)
        for h in __has_list:
            self.__results.append(self.__datas[h])

    def __classification(self):
        ans = []
        __MAX_DIST = 442 #math.sqrt((255-0)**2 + (255-0)**2 + (255-0)**2) < 442
        for d in self.__datas:
            __dist = __MAX_DIST
            __pos = 0
            for ri, r in enumerate(self.__results):
                __ = math.sqrt(
                        (d[0] - r[0])**2 +
                        (d[1] - r[1])**2 +
                        (d[2] - r[2])**2)
                if __ < __dist:
                    __dist = __
                    __pos = ri
                else:
                    pass
            ans.append(__pos)
        self.__assign = ans

    def __barycenter(self):
        __dict = {}
        for vi, v in enumerate(self.__results):
            __dict[vi] = []
        for ai, a in enumerate(self.__assign):
            __dict[a].append(self.__datas[ai])
        for vi, v in enumerate(self.__results):
            __ = [0, 0, 0]
            for j, w in enumerate(__dict[vi]):
                __[0] += __dict[vi][j][0]
                __[1] += __dict[vi][j][1]
                __[2] += __dict[vi][j][2]
            __div = len(__dict[vi])
            if __div == 0:
                __rgb = (__[0], __[1], __[2])
            else:
                __rgb = (__[0]/__div, __[1]/__div, __[2]/__div)
            self.__results[vi] = __rgb

    def __is_end(self):
        flag = False
        for vi, v in enumerate(self.__justbefore):
            if ((self.__results[vi][0] - v[0]) +
                    (self.__results[vi][1] - v[1]) +
                    (self.__results[vi][2] - v[2]) <= 0.0):
                flag = True
        if flag == True:
            return True
        else:
            return False

    def run(self, k):
        self.__k = k
        self.__initialization()
        print("DEBUG kmeanspp.py: 1st __results => {0}".format(self.__results))
        while True:
            self.__justbefore = copy.deepcopy(self.__results)
            self.__classification()
            self.__barycenter()
            if self.__is_end() is True:
                for i in self.__results:
                    __ = []
                    for ii in i:
                        __.append(int(round(ii)))
                    self.results.append(tuple(__))
                self.assign = self.__assign
                break

if __name__ == '__main__':
    """ Test code
    :let b:quickrun_config={'args': '_in.png _out.png'}
    """
    if len(sys.argv) != 3:
        print("Usage: $ python KMeansPP.py <input> <output>")
        sys.exit(-1)
    print("input => {0}, output => {1}".format(sys.argv[1], sys.argv[2]))
    datas = [
            (0, 255, 255),
            (127, 255, 255),
            (255, 255, 0),
            (255, 127, 0),
            (255, 127, 255),
            (255, 0,   255),
            (127, 127, 127),
            (255, 255, 255),]
    kmpp = KMeansPP(datas)
    kmpp.run(2)
    print("kmpp.results => {0}".format(kmpp.results))
    print("kmpp.assign => {0}".format(kmpp.assign))
