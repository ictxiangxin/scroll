__author__ = 'ict'

from calculate.distance import euclid
from calculate.distance import manhattan
from calculate.distance import chebyshev
from calculate.distance import minkowski
from calculate.distance import cos
from calculate.distance import pearson

callback_index = 0
option_indx = 1

method_set = {
    "euclid": (euclid, False),
    "manhattan": (manhattan, False),
    "chebyshev": (chebyshev, False),
    "minkowski": (minkowski, True),
    "cos": (cos, False),
    "pearson": (pearson, False)
}


def method(mtd, data_a, data_b, option=None):
    if len(data_a) != len(data_b):
        raise Exception("Two vecter must have same dimension")
    mtd_list = mtd.split(",")
    for i in range(len(mtd_list)):
        while True:
            if len(mtd_list[i]) == 0:
                raise Exception("Miss method")
            if mtd_list[i][0] == " ":
                mtd_list[i] = mtd_list[i][1:]
            if mtd_list[i][-1] == " ":
                mtd_list[i] = mtd_list[i][:-1]
            if mtd_list[i][0] != " " and mtd_list[i][-1] != " ":
                break
    if len(mtd_list) == 1:
        option = [option]
    if option is None:
        option = [None] * len(mtd_list)
    rst = []
    for i in range(len(mtd_list)):
        if mtd_list[i] not in method_set:
            raise Exception("No such distance mothod: " + str(mtd_list[i]))
        if method_set[mtd_list[i]][option_indx] and option[i] is not None:
            if isinstance(option[i], dict):
                rst.append(method_set[mtd_list[i]][callback_index].compute(data_a, data_b, **option[i]))
            else:
                rst.append(method_set[mtd_list[i]][callback_index].compute(data_a, data_b, option[i]))
        else:
            rst.append(method_set[mtd_list[i]][callback_index].compute(data_a, data_b))
    if len(rst) == 1:
        return rst[0]
    else:
        return rst


def get_function(mtd):
    if mtd not in method_set:
        raise Exception("No such cluster method: " + str(mtd))
    return method_set[mtd][callback_index].compute


def names():
    return list(method_set)