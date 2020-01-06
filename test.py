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



def window_capture(filename):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    #w = w/4
    #h = h/20
    print w,h
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

time.sleep(2)
beg = time.time()
window_capture("haha.jpg")
end = time.time()
print(end - beg)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
image = cv2.imread("haha.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("test.jpg", gray)
text = pytesseract.image_to_string(Image.open("test.jpg"))
print text
