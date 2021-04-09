# -*- coding: utf-8 -*-
import cv2

import pytesseract
from PIL import Image
import time
# pic = cv2.imread(r"D:\MyWorkSpace\AutoMouse\test2.PNG", cv2.IMREAD_COLOR)
# picGray = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
# re, picThresh = cv2.threshold(picGray, 127, 255, 0)
def test():
    image = Image.open(r"E:\ChromeDownloads\androidscreencast-0.0.16s\app.png")
    text = pytesseract.image_to_string(image, lang='chi_sim')  # 使用简体中文解析图片
    print(text)
#cv2.imshow('picThresh', picGray)
#cv2.waitKey()
start = time.clock()
test()
print(time.clock() - start)


