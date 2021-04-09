# -*- coding: utf-8 -*-
from copy import deepcopy

bakop = []

def operation(operator, res, factor):
    ret = -1
    if type(res) is not int or res < 1:
        # raise Exception("Invalid operation %s %s %s" % (operator, factor, res))
        return -1
    bakop.append(operator)
    if "+" == operator:
        ret = res + factor
    if '-' == operator:
        ret = res - factor
    if '*' == operator:
        ret = res * factor
    if '/' == operator:
        ret = res / factor
    return ret

def get24(inputall):
    operator = ['+', '-', '*', '/']
    for a in inputall:
        m1 = deepcopy(inputall)
        m1.remove(a)
        lefta = deepcopy(m1)
        for b in lefta:
            for i in operator:
                sum = operation(i, a, b)
                m2 = deepcopy(lefta)
                m2.remove(b)
                leftb = deepcopy(m2)
                for c in leftb:
                    for i in operator:
                        ret = operation(i, sum, c)
                        if ret == -1:
                            continue
                        else:
                            sum = ret
                        m3 = deepcopy(leftb)
                        m3.remove(c)
                        leftc = deepcopy(m3)
                        for d in leftc:
                            for i in operator:
                                ret = operation(i, sum, d)
                                if ret == -1:
                                    continue
                                else:
                                    sum = ret
                                    if sum == 24:
                                        print("get 24: %d %s %d %s %d %s %d" % (a,
                                                                                bakop[0],
                                                                                b,
                                                                                bakop[1],
                                                                                c,
                                                                                bakop[2], d))

                                        return
                                bakop = []

get24([2, 2, 10, 4])
