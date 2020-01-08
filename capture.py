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
    #print 'left ', left
    #print 'right ',right
    #print 'top ', top
    #print 'bottom ', bottom
    right = int(right*1.77)
    left = int(left*1.77)
    bottom = int(bottom*1.77)
    top  = int(top*1.77)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    w = right - left
    h = bottom - top
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

def _snap_handle(filename, filename2):
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

#bt old old
#bt dmd new
#bt mmo semi
#bt mpo finish
def newbattle():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    _window_capture("full.jpg")
    _snap_handle("full.jpg", "minimal.jpg")
    text = pytesseract.image_to_string(Image.open("minimal.jpg"))
    print text
    try:
        t = str(text).splitlines()
        if len(t) >= 1:
            for i in 0, len(t)-1:
                if t[i].find("old") >= 0:
                    print 'old'
                    return False
                else:
                    print 'new'
                    return True
        return False
    except:
        return False

def endbattle():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    _window_capture("full.jpg")
    _snap_handle("full.jpg", "minimal.jpg")
    text = pytesseract.image_to_string(Image.open("minimal.jpg"))
    print text
    t = str(text).splitlines()
    try:
        if len(t) >=1:
            for i in 0, len(t)-1:
                if t[i].find("mpo") >= 0:
                    print 'finish'
                    return True
            return False
        return False
    except:
        return False
        
time.sleep(2)
_window_capture("hahaha.jpg")
_snap_handle("hahaha.jpg", "test.jpg")