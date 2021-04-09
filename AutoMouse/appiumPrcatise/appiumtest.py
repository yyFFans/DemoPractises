# -*- coding: utf-8 -*-
from appium import webdriver
import time

import os
print(os.getenv('ANDROID_SDK_ROOT'))
testingconfig = {}

testingconfig["platformName"] = 'Android'
testingconfig['platformVersion'] = '8.1.0'
testingconfig['deviceName'] = 'MI5X'
# testingconfig['app'] = ''
testingconfig['appPackage'] = 'com.p1.mobile.putong'
testingconfig['appActivity'] = 'com.p1.mobile.putong.ui.splash.SplashProxyAct'
testingconfig['unicodeKeyboard'] = True
testingconfig['resetKeyboard'] = True
testingconfig['noReset'] = True
testingconfig['newCommandTimeout'] = 6000

driver = webdriver.Remote("http://localhost:4723/wd/hub", testingconfig)



