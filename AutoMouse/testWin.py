# -*- coding: utf-8 -*-
num = [1, 3, 7, 8]


def calc(left):
    if left == 1:
        return True

    maxa = left
    maxb = (left) // 3
    maxc = (left) // 7
    maxd = (left) // 8

    allRes = []
    for a in range(maxa + 1):
        for b in range(maxb + 1):
            for c in range(maxc + 1):
                for d in range(maxd + 1):
                    sum = a + b * 3 + c * 7 + d * 8

                    if sum == (left - 1):
                        allRes.append([a, b, c, d])

    if allRes != []:
        for m in allRes:
            print(m)
            if (m[0] + m[1] + m[2] + m[3]) % 2 == 1:
                # print(m)
                return False
        return True
    else:
        return False

def AWin(N):
    for i in num:
        # print(i)
        if N > i:
            if calc(N-i) == True:
                print("first %d" % i)
                return True
    return False

AWin(14)

def test(N):
    for i in range(N):
        if AWin(i):
            print("%d AWin" % i)

# test(20)