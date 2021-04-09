# -*- coding: utf-8 -*-

MEM = {}


def pick(i, total):
    return total - i


CNT = 0


def howManyWays(total, rangestart):
    global CNT
    if rangestart > total:
        return

    print("total:%d, rangestart:%d" % (total, rangestart))
    for i in range(rangestart, total + 1):
        n = total // i
        for j in range(1, n + 1):
            CNT = CNT + 1
            left = total - j * i
            if left >= rangestart+1:
                howManyWays(left, rangestart + 1)
    print(CNT)

howManyWays(6, 2)
print("%d cnt：%d" % (6, CNT+1))
