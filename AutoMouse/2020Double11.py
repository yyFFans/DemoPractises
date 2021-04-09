# -*- coding: utf-8 -*-

"""
运行前需先自行进入淘宝双十一领喵币中心

截屏识别出 按钮位置

手机操作 adb input
input keyevent 93 -- 向下翻页
input keyevent 4 -- 返回

截图并传到PC
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png D:\tmp

利用eastocr 来识别按钮位置

遇到的坑：依赖的torch版本问题
pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f
https://download.pytorch.org/whl/torch_stable.html

Downloading detection model, please wait
"""

pic = r"D:\tmp\test.png"


import easyocr

reader = easyocr.Reader(
    ['ch_sim', 'en'])  # need to run only once to load model into memory
result = reader.readtext(pic)
print(result)