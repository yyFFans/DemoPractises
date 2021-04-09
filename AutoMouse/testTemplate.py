# -*- coding: utf-8 -*-
import cv2
import numpy as np

template = cv2.imread(r"D:\MyWorkSpace\AutoMouse\pics\jump.PNG", cv2.IMREAD_COLOR)
template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
ret, template = cv2.threshold(template, 127, 255, 0)

pic = cv2.imread(r"D:\MyWorkSpace\AutoMouse\testJump1.PNG", cv2.IMREAD_COLOR)
picGray = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
re, picThresh = cv2.threshold(picGray, 127, 255, 0)

h, w = template.shape[:2]  # rows->h, cols->w
print(h,w)

cv2.imshow('picThresh', picThresh)
cv2.imshow('template', template)
res = cv2.matchTemplate(picThresh, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print(type(res))
res2 = np.ndarray(res.shape)
#print(res)
cv2.normalize(res, res, 1.0, 0.0, cv2.NORM_MINMAX)
print(res)
loc = np.where(res >= 0.8)
print(loc)
#print(res)
print(min_val, max_val, min_loc, max_loc)


left_top = max_loc  # 左上角
right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
cv2.rectangle(pic, left_top, right_bottom, 100, 2)  # 画出矩形位置

cv2.imshow("template res", pic)
cv2.waitKey()