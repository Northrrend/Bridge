# -*- coding: utf-8 -*-
import win32gui, win32ui, win32con, win32api
import pytesseract
import cv2
from PIL import Image


def _to_real_pos(pos):
    return int(float(pos) / SCREEN_SCALE)

def init_wow_window_pos(w, h):
    handle = win32gui.FindWindow("GxWindowClass", None)
    print "WOW window id = %s" % handle
    if handle == 0:
        print "Can not find Wow window!"
        return False
    else:
        win32gui.SetForegroundWindow(handle)
        win32gui.MoveWindow(handle, _to_real_pos(0), _to_real_pos(0), _to_real_pos(w), _to_real_pos(h), True)
        win32gui.SetForegroundWindow(handle)
        return True

def _window_capture(filename):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    x1 = -(GAME_W*55/1960)
    y1 = -(GAME_H*664/1080)
    x2 = GAME_W*634/1960
    y2 = GAME_H*839/1080
    w = x1 + x2
    h = (y1 + y2)/6
    y1 = -(y2 - h)
    saveBitMap.CreateCompatibleBitmap(mfcDC, int(w), int(h))
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((int(x1), int(y1)), (int(x2), int(y2)), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

def _snap_cut(filename, filename2):
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
    _snap_handle("full.jpg", "gray.jpg")
    text = pytesseract.image_to_string(Image.open("gray.jpg"))
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
    except UnicodeEncodeError:
        #k = PyKeyboard()
        #k.tap_key(k.enter_key)
        #account.login()
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
