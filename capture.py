# -*- coding: utf-8 -*-
import win32gui, win32ui, win32con, win32api
import pytesseract
import cv2
from PIL import Image
import os

class Eye(object):

    def __init__(self):   
        self.VIRTUAL = 1
        self.SCREEN_SCALE = 2.0
        self.SCREEN_W = 3840
        self.SCREEN_H = 2160
        self.GAME_SCALE = 0.9
        self.GAME_W = self.SCREEN_W*self.GAME_SCALE
        self.GAME_H = self.SCREEN_H*self.GAME_SCALE
        p = os.popen('Systeminfo | findstr /i "System Model"')
        t = p.read()
        if t.find('VMware') > 0 :
            pass
        else:
            self.VIRTUAL = 0
        if not self.init_wow_window_pos():
            print('Locate wow window failed exit')
            exit(-1)

    def _to_real_pos(self, pos):
        scale = self.SCREEN_SCALE
        return int(float(pos) / scale)

    def init_wow_window_pos(self):
        w = self.GAME_W
        h = self.GAME_H
        handle = win32gui.FindWindow("GxWindowClass", None)
        print "WOW window id = %s" % handle
        if handle == 0:
            print "Can not find Wow window!"
            return False
        else:
            if self.VIRTUAL == 0:
                win32gui.SetForegroundWindow(handle)
                win32gui.MoveWindow(handle, self._to_real_pos(0), self._to_real_pos(0), self._to_real_pos(w), self._to_real_pos(h), True)
            win32gui.SetForegroundWindow(handle)
            return True

    def _window_capture(self, filename):
        hwnd = 0
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        if self.VIRTUAL == 1:
            x1 = 0
            y1 = 0
            x2 = 200
            y2 = 30
        if self.VIRTUAL == 0 :
            x1 = -9/self.SCREEN_SCALE
            y1 = -150/self.SCREEN_SCALE
            x2 = 400
            y2 = 90/self.SCREEN_SCALE - y1
        w = x1 + x2
        h = y1 + y2
        saveBitMap.CreateCompatibleBitmap(mfcDC, int(w), int(h))
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((int(x1), int(y1)), (int(x2), int(y2)), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, filename)

    def _snap_cut(self, filename, filename2):
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

    def _snap_handle(self, filename, filename2):
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(filename2, gray)

    def dashboard(self, code_list):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        self._window_capture("full.jpg")
        self._snap_handle("full.jpg", "gray.jpg")
        text = pytesseract.image_to_string(Image.open("gray.jpg"))
        print "DASHBOARD == " + text + " =="
        try:
            for code in code_list:
                if text.find(code) >= 0:
                    return code
        except:
            return "NULL"
        return "NULL"