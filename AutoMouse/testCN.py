# -*- coding: utf-8 -*-

testStrings = """:: 这是一个例子
#relative or absolute path to ADB
adb.path=./adb.exe
:: another 例子
#maximum time to wait for device (in seconds)
#adb.device.timeout=30
#maximum time to execute adb command (in seconds)
#adb.command.timeout=5
#app.window.width=1024
#app.window.height=768
#Defines whether application should look 'natively' to OS
#app.native.look=false
"""

with open("template.cmd","w") as f:
    f.write(testStrings)
