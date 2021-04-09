#一种王者荣耀刷金币方法


###所用工具环境
* python3.6.5 和 支持自动鼠标键盘点击等编程的pyautogui功能包 
* windows PC，安卓模拟器bluestacks，安装王者荣耀

###基本思路
王者荣耀有闯关任务模式可以获得金币，任务两三分钟一般就可以完成，支持自动模式，一次可获取三四十金币，且可以重复刷取。

利用脚本，模拟任务开启点击，进入后自动执行，中间对话跳过，最后任务完成检测，再次启动任务。均是通过截屏信息获取当前在做什么，然后应该点击什么，如此往复执行。

###脚本所用关键功能说明
pyautogui.screenshot 用于截屏。
下面是py doc中函数原型，可传入文件名，最终返回截屏图片，保存在本地

    screenshot = _screenshot_win32(imageFilename=None)

pyautogui.locateOnScreen  用于查找局部图片位置（像素点区域位置）。输入图片文件名，最终返回图片所在位置，如果当前屏幕不存在该图片，则返回None

	locateOnScreen(image, grayscale=False, region=None)

事先截取好中间需要点击的按钮图片，保存在本地，然后截屏中去匹配查找按钮图片是否存在及其位置（该函数实际并不需要事先调用screenshot）

pyautogui.center 用于获取某一像素区域的中心像素点位置。

	center(coords)


###源文件
![文件](D:\MyWorkSpace\AutoMouse\src.PNG)

pics中是事先截取的
![预先截取的图片](D:\MyWorkSpace\AutoMouse\pics.PNG)

参见百度云盘 https://pan.baidu.com/s/1TspfdYdSwnAvlt0iC4BfxQ 密码: 3q6v

###实际运行效果展示
最开始选用最后一个关卡任务（大师级）
![初始](D:\MyWorkSpace\AutoMouse\1st.PNG)

下一步，进入任务后，再启用脚本
![预先截取的图片](D:\MyWorkSpace\AutoMouse\2st.PNG)

后面就自动执行了

###源码展示
很简单，重在功能，没有注重什么规范
（业余python选手，工作之中也是python用于内部工具开发,代码槽点可能较多）。

	# -*- coding: utf-8 -*-

    import pyautogui
    import time

    pyautogui.FAILSAFE = False
    screenshot = pyautogui.screenshot

    pngLocate = pyautogui.locateOnScreen

    def click(x,y):
        pyautogui.moveTo(x,y)

        pyautogui.click()

    def get_button_center_from_screen(button_png,png_path='pics'):
        screen = screenshot("screen.png")
        button_png = png_path + '\\' + button_png
        start_pos = pngLocate(button_png)

        if start_pos == None:
            #找不到button
            print("{} not exsit on current screen".format(button_png))
            return 0,0

        return pyautogui.center(start_pos)

    def AutoMouse():

        print("Start")

        n = 1

        while(n<60):

            print("{now} 第{n}次\n".format(now=time.strftime("%m-%d %H:%M:%S"), n=n))

            x, y = get_button_center_from_screen('开始闯关.PNG')
            click(x,y)
            time.sleep(5)

            loading = False
            #是否正在加载中
            while(1):
                x,y = get_button_center_from_screen('加载中.PNG')
                time.sleep(3)
                if (x,y) != (0,0):
                    break

            loading = False
            print("加载中\n")

            while(1):
                x,y = get_button_center_from_screen('加载中.PNG')
                if (x,y) == (0,0):
                    break

            print("加载完成\n")


            #检查是否初始画面需要跳过
            x,y = get_button_center_from_screen('跳过.PNG')
            if (x,y) == (0,0):
                print("no need Jump over")
            else:
                print("need Jump over")
                click(x,y)

            #检查是否已经启用自动
            x,y = get_button_center_from_screen("未启用自动.PNG")
            if (x,y) != (0,0):
                print("not auto run")
                click(x,y)
            else:
                print("already auto run")


            #运行监测，是否结束，以及中间存在需要跳过，结束则开启下一次  每5s检测一次
            while(1):
                time.sleep(3)
                x,y = get_button_center_from_screen('跳过2.PNG')
                if (x,y) == (0,0):
                    print("no need Jump over")
                else:
                    print("need Jump over")
                    click(x,y)

                x,y = get_button_center_from_screen("结束后继续.PNG")
                if (x,y) == (0,0):
                    print("not over")
                else:
                    print("all over.\n")
                    click(x,y)
                    time.sleep(5)

                    #start 闯关
                    print("Start again")
                    x, y = get_button_center_from_screen('再次挑战.PNG')
                    n = n+1
                    click(x,y)
                    time.sleep(10)
                    break

    if __name__ == '__main__':
        AutoMouse()


###注意事项
 1. 脚本可能需要在管理员权限下执行（cmd启动时以管理员身份运行）（click执行没有效果的时候，就是权限问题导致的）
 2. 由于电脑尺寸可能不是绝对一样，所以事先截取的按钮图片可能都不一样，自行截取个人PC上实际王者荣耀刷任务运行时画面，对应替换
 3. 个人在使用过程中遇到过的问题：
     * 有一次晚上挂机，电脑死过机，应该和这个没关系。。。
     * 安卓模拟器中的王者荣耀出现卡机（手动点击也是没有反应，最后只好重启了模拟器），不知有没有关系
     * 加载图片 匹配不到，原因是王者荣耀有更新，任务开始后加载页面的广告有变化，建议截取关键按钮时，尽量截取小部分，不要截取太多。

