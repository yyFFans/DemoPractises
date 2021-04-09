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

    while(n<90):
        
        print("{now} 第{n}次\n".format(now=time.strftime("%m-%d %H:%M:%S"), n=n))

        while(1):
            x, y = get_button_center_from_screen('开始闯关.PNG')
            if (x,y) == (0,0):
                time.sleep(2)
                continue
            
            click(x,y)
            time.sleep(5)
            break

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
        if 0:    
            #检查是否已经启用自动
            x,y = get_button_center_from_screen("未启用自动.PNG")
            if (x,y) != (0,0):
                print("not auto run")
                click(x,y)
            else:
                print("already auto run")
            
        time.sleep(80)
        #运行监测，是否结束，以及中间存在需要跳过，结束则开启下一次  每5s检测一次

        JumpOver_1 = False
        JumpOver_2 = False

        Game_END = False
        while(1):


            if JumpOver_1 == False:

                x,y = get_button_center_from_screen('秦始皇1跳过.PNG')
                if (x,y) != (0,0):
                    print("need Jump over 1")
                    JumpOver_1 = True
                    click(x,y)

            if JumpOver_2 == False:
                x, y = get_button_center_from_screen('秦始皇2跳过.PNG')
                if (x, y) != (0, 0):
                    print("need Jump over 2")
                    JumpOver_2 = True
                    click(x, y)

            if JumpOver_1 == True or JumpOver_2 == True:
                x,y = get_button_center_from_screen("结束后继续.PNG")
                if (x,y) != (0,0):
                    print("all over.\n")
                    Game_END = True
                    click(x,y)

                
                #start 闯关
                if Game_END == True:

                    x, y = get_button_center_from_screen('再次挑战.PNG')
                    if (x, y) != (0, 0):
                        n = n+1
                        print("Start again")
                        click(x,y)
                        time.sleep(2)
                        break

if __name__ == '__main__':
    AutoMouse()

