# -*- coding: utf-8 -*-
import win32gui, win32ui, win32con, win32api
import pytesseract
import cv2
from PIL import Image

VIRTUAL = 1
SCREEN_SCALE = 1.25
SCREEN_W = 1920
SCREEN_H = 1080
GAME_SCALE = 0.8
GAME_W = SCREEN_W*GAME_SCALE
GAME_H = SCREEN_H*GAME_SCALE

def _to_real_pos(pos):
    scale = SCREEN_SCALE
    return int(float(pos) / scale)

def init_wow_window_pos():
    w = GAME_W
    h = GAME_H
    handle = win32gui.FindWindow("GxWindowClass", None)
    print "WOW window id = %s" % handle
    if handle == 0:
        print "Can not find Wow window!"
        return False
    else:
        if VIRTUAL == 0:
            win32gui.SetForegroundWindow(handle)
            win32gui.MoveWindow(handle, _to_real_pos(0), _to_real_pos(0), _to_real_pos(w), _to_real_pos(h), True)
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
    x1 = -30
    y1 = -30
    x2 = 300
    y2 = 403
    w = x1 + x2
    h = y1 + y2
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
    if VIRTUAL == 1:
        x1 = 0
        y1 = 0
        x2 = 200
        y2 = 30
    if VIRTUAL == 0 :
        x1 = -9
        y1 = -40
        x2 = 200/SCREEN_SCALE
        y2 = 30/SCREEN_SCALE - y1
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
    if VIRTUAL == 1:
        _window_capture3("full.jpg")
    else:
        _window_capture("full.jpg")
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
    if VIRTUAL == 1:
        _window_capture3("full.jpg")
    else:
        _window_capture("full.jpg")
    text = pytesseract.image_to_string(Image.open("full.jpg"))
    #print text
    try:
        if text.find("MMO") >= 0:
            return True
    except:
        return False
    return False

def dashboard():
    code_list = ["MMO","OLD","BTO","SEMI","MPP"]
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    _window_capture3("full.jpg")
    _snap_handle("full.jpg", "gray.jpg")
    text = pytesseract.image_to_string(Image.open("gray.jpg"))
    print "DASHBOARD == " + text + " =="
    try:
        for code in code_list:
            if text.find(code) >= 0:
                return code
    except:
        return "NULL"
    return "NULL"