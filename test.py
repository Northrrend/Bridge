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


time.sleep(2)
warrior = Role()
warrior.turn_left(0.15)
warrior.march(2.8)
warrior.donate_ws()



