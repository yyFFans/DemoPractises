# -*- coding: utf-8 -*-
from unittest import result

import cv2
import pytesseract
from PIL import Image
import numpy


img = cv2.imread(r"D:\MyWorkSpace\AutoMouse\pics\loading2.PNG",cv2.IMREAD_COLOR)
#print(img)
grayImg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
#img = Image.open(r"D:\MyWorkSpace\AutoMouse\pics\loading.PNG")
#s = pytesseract.image_to_string(img, lang='chi_sim')
#print(grayImg)

ret, thresh = cv2.threshold(grayImg, 127, 255, 0)
cv2.imshow('gray img', grayImg)
cv2.imshow('thresh img', thresh)

pic = cv2.imread("D:\MyWorkSpace\AutoMouse\pics.PNG", cv2.IMREAD_COLOR)
grayPic = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
re, threshPic = cv2.threshold(grayPic, 127, 255, 0)
cv2.imshow('pic gray img', grayPic)
cv2.imshow('thresh pic', threshPic)
cv2.waitKey()
#print(s)

