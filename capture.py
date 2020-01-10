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

def _window_capture(filename):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    hwnd1 = win32gui.FindWindow(0, u'魔兽世界')
    #hwndDC = win32gui.GetWindowDC(hwnd1)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd1)
    right = int(right*2)
    left = int(left*2)
    bottom = int(bottom*2)
    top  = int(top*2)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    w = right - left
    h = bottom - top
    x1 = -65
    y1 = -935
    x2 = 742
    y2 = 987
    w = x1 + x2
    h = y1 + y2
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((x1, y1), (x2, y2), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

def _snap_handle2(filename, filename2):
    image = cv2.imread(filename)
    h = image.shape[0]
    w = image.shape[1]
    x0 = int(w*0.02)
    x1 = int(w*0.27)
    y0 = int(h*0.84)
    y1 = int(h*0.96)
    cropped = image[y0:y1, x0:x1]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filename2, gray)

def _snap_handle(filename, filename2):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filename2, gray)

#bt old old
#bt dmd new
#bt mmo semi
#bt mpo finish
def newbattle():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    _window_capture("full.jpg")
    text = pytesseract.image_to_string(Image.open("full.jpg"))
    try:
        print text
        if text.find("old") >= 0:
            return False
        elif text.find("dmd") >= 0:
            return True
        elif text.find("mmo") >= 0:
            return True
        else:
            return False
    except:
        return False

def endbattle():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    _window_capture("full.jpg")
    text = pytesseract.image_to_string(Image.open("full.jpg"))
    print text
    try:
        if text.find("mpo") >= 0:
            return True
    except:
        return False
    return False
