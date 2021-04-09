# -*- coding: utf-8 -*-
from random import choices
from collections import OrderedDict
inputs = input("请输入爱的宣言：\n")
loveString = "愿得一人心白首不相离爱你一万年月亮代表我的心恨不相逢未嫁时"

inputs = ''.join(OrderedDict.fromkeys(inputs))

if len(inputs) < 10:
    for char in loveString:
        if char in inputs:
            loveString = loveString.replace(char, '')
    leftCharCnt = 10 - len(inputs)
    leftchars = choices(loveString, k=leftCharCnt)
    for i in range(leftCharCnt):
        inputs += leftchars[i]

numbers = "零一二三四五六七八九"
basecodecs = dict()

for i in range(10):
    basecodecs[numbers[i]] = inputs[i]

keys = input("输入 Pony Ma 发的账号:\n")
while keys.isdigit() != True:
    keys = input("输入有误, 请输入 Pony Ma 发的账号:\n")

loveSec = ''

for k in keys:
    loveSec += basecodecs[numbers[int(k)]]

# print(inputs, '\n', loveSec)
print('')
print(inputs)
for k,v in basecodecs.items():
    print(v,':',k)
print('')
print("秘语：" + loveSec)





