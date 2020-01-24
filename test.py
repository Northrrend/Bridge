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

time.sleep(2)

virtual = 1
SCREEN_SCALE = 1.25
SCREEN_W = 1960
SCREEN_H = 1080
GAME_SCALE = 0.8
GAME_W = SCREEN_W*GAME_SCALE
GAME_H = SCREEN_H*GAME_SCALE

if not capture.activate_wow_window():
        print('Locate wow window failed exit')
        exit(-1)
time.sleep(2)
capture._window_capture3("hahaha.jpg")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
text = pytesseract.image_to_string(Image.open("hahaha.jpg"))
print text

warrior = Role()
warrior.donate()
