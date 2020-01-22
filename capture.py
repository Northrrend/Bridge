# -*- coding: utf-8 -*-
import win32gui, win32ui, win32con, win32api
import pytesseract
import cv2
from PIL import Image

SCREEN_SCALE = 1.25
SCREEN_W = 1920
SCREEN_H = 1080
GAME_SCALE = 0.8
GAME_W = SCREEN_W*GAME_SCALE
GAME_H = SCREEN_H*GAME_SCALE

def _to_real_pos(pos, scale):
    return int(float(pos) / scale)

def init_wow_window_pos(w, h, scale):
    handle = win32gui.FindWindow("GxWindowClass", None)
    print "WOW window id = %s" % handle
    if handle == 0:
        print "Can not find Wow window!"
        return False
    else:
        win32gui.SetForegroundWindow(handle)
        win32gui.MoveWindow(handle, _to_real_pos(0, scale), _to_real_pos(0, scale), _to_real_pos(w, scale), _to_real_pos(h, scale), True)
        win32gui.SetForegroundWindow(handle)
        return True

def activate_wow_window():
    handle = win32gui.FindWindow("GxWindowClass", None)
    print "WOW window id = %s" % handle
    if handle == 0:
        print "Can not find Wow window!"
        return False
    else:
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

def _window_capture3(filename):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    x1 = 0
    y1 = 0
    x2 = 200 * SCREEN_SCALE
    y2 = 30 * SCREEN_SCALE
    w = x1 + x2
    h = y1 + y2
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

def newbattle():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    _window_capture3("full.jpg")
    text = pytesseract.image_to_string(Image.open("full.jpg"))
    try:
        #print text
        if text.find("OLD") >= 0:
            return False
        elif text.find("SEMI") >= 0:
            return True
        elif text.find("BTO") >= 0:
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
    _window_capture3("full.jpg")
    text = pytesseract.image_to_string(Image.open("full.jpg"))
    #print text
    try:
        if text.find("END") >= 0:
            return True
    except:
        return False
    return False
