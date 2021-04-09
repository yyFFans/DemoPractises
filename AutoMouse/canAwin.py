# -*- coding: utf-8 -*-

num = [1, 3, 7, 8]

numadd = {1: [2, 4, 8, 9], 3: [4, 6, 10, 11], 7: [8, 10, 14, 15], 8: [9, 11, 15, 16]}

for i in num:
    numadd[i] =
    for j in num:
        numadd[i].append(i+j)

memRecorda = set()

def canPickAB(a, left):
    if left > numadd[a][0]:
        return True

def pick(N):
    # B取完后剩下0个或者1个 A loose
    if N == 0 or N == 1:
        return False

    # first A
    for i in num:
        left = N - i
        if left > 0:
            for j in numadd[i]:
                left = left - j
                if left > 0:



def cal(left):
    if left == 1:
        return True
    elif left == 0:
        return False
    else:
        res = []
        for i in numadd:
            if left >= i:
                res.append(cal(left - i))
        if False in res:
            return False
        else:
            return True

def AWin(N):
    for i in num:
        if N > i:
            if cal(N -i ) == True:
                return True
    return False

print(AWin(17))

for i in range(1000):
    print(i)
    if AWin(i):
        print("%d A Win" % i)

# memRecord = []
#
#
# def calc(N):
#     if N in memRecord:
#         return True
#     if N == 1:
#         return True
#     for i in num:
#         if N<i:
#             break
#         left = N - i
#         maxa = left - 1
#         maxb = (left - 1) // 3
#         maxc = (left - 1) // 7
#         maxd = (left - 1) // 8
#
#         allRes = []
#         for a in range(maxa + 1):
#             for b in range(maxb + 1):
#                 for c in range(maxc + 1):
#                     for d in range(maxd + 1):
#                         sum = a + b * 3 + c * 7 + d * 8
#                         if sum == left - 1:
#                             allRes.append([a, b, c, d])
#         needRecalc = False
#         if allRes != []:
#             for m in allRes:
#                 if (m[0] + m[1] + m[2] + m[3]) % 2 == 0:
#                     needRecalc = True
#                     break
#             if needRecalc:
#                 pass
#             else:
#                 memRecord.append(N)
#                 return True
#         return False
#     return False
#
#
# def canAWin(N):
#     for i in num:
#         if N > i:
#             return calc(N - i)
#
# for i in range(10):
#     if canAWin(i):
#         print("%d A Win" % i)