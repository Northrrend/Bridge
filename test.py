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

def window_capture(filename):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    hwnd1 = win32gui.FindWindow(0, "Command Prompt")
    left, top, right, bottom = win32gui.GetWindowRect(hwnd1)
    print right
    print left
    print bottom
    print top
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    w = right - left
    h = bottom - top
    print w,h
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (right, bottom), mfcDC, (left, top), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

time.sleep(0.5)
beg = time.time()
window_capture("haha.jpg")
end = time.time()
print(end - beg)

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
#image = cv2.imread("ori.jpg")
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imwrite("con.jpg", gray)
#text = pytesseract.image_to_string(Image.open("con.jpg"))
#print text
