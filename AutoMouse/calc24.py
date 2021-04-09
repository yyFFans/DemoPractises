# -*- coding: utf-8 -*-
class Operation:
    def __init__(self, inputNumList, operatorList):
        self.a = inputNumList[0]
        self.b = inputNumList[1]
        self.c = inputNumList[2]
        self.d = inputNumList[3]

        self.op1 = operatorList[0]
        self.op2 = operatorList[1]
        self.op3 = operatorList[2]

        def calc(a, b , op):
            if "+" == op:
                ret = a + b
            elif '-' == op:
                ret = a - b
            elif '*' == op:
                ret = a * b
            elif '/' == op:
                ret = a / b
            else:
                ret = -1
            return ret

        res = calc(self.a, self.b, self.op1)
        if res == -1:
            self.res = -1
            return
        else:
            res = calc(res, self.c, self.op2)
            if res == -1:
                self.res = -1
                return
            else:
                self.res = calc(res, self.d, self.op3)

def calc24(inputs):
    from copy import deepcopy
    operator = ["+", "-", "*", "/"]
    inputLists = set()
    operatorLists = []
    for a in inputs:
        ma = deepcopy(inputs)
        ma.remove(a)
        for b in ma:
            mb = deepcopy(ma)
            mb.remove(b)
            for c in mb:
                mc = deepcopy(mb)
                mc.remove(c)
                for d in mc:
                    inputLists.add((a,b,c,d))

    for op1 in operator:
        for op2 in operator:
            for op3 in operator:
                operatorLists.append((op1,op2,op3))


    for numList in inputLists:
        for opList in operatorLists:
            operation = Operation(numList, opList)
            if operation.res == 24:
                print("get 24: %d %s %d %s %d %s %d" % (operation.a,operation.op1,
                                                        operation.b,operation.op2,
                                                        operation.c,operation.op3,
                                                        operation.d))
                return
    print("无法计算出24")

#calc24([2,2,10,4])

while 1:
    inputs = input("请输入4个数：\n")

    inputs.split()

    inputLists = [int(m) for m in inputs.split()]

    calc24(inputLists)


