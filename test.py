# -*- coding: utf-8 -*-
import time
import io
import win32gui, win32ui, win32con, win32api
import sys
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  
from PIL import Image
import pytesseract
import argparse
import cv2
import os
from ctypes import *
from ctypes.wintypes import *
import ctypes
import account
import KeymouseGo
from role import Role
import capture
from capture import *


p = os.popen('Systeminfo | findstr /i "System Model"')
t = p.read()
if t.find('VMware') > 0 :
    print 'vm'
else:
    print 'baremental'
        

if not init_wow_window_pos():
        print('Locate wow window failed exit')
        exit(-1)
time.sleep(2)



