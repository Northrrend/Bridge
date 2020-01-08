# -*- coding: UTF-8 -*-

import win32gui
from PIL import Image
from PIL import ImageGrab
import time


SCREEN_SCALE = 2.00
JoinDialogBbox = (909, 212, 1240, 298)
JoinImgName = "JoinImgFlg.png"
LeaveDialogBbox = (985, 810, 1216, 846)
LeaveImgName = "LeaveImgFlg.png"
EscapeIconBbox = (1864, 193, 1896, 226)
EscapeIconName = "EscapeIcon.png"
PrepareEnterBboxList = [(255, 445, 364, 466), (255, 429, 364, 445), (255, 411, 364, 429),
                        (255, 395, 364, 411), (255, 378, 364, 395)]
PrepareImgName = ["PrepareImgFlg1.png", "PrepareImgFlg2.png", "PrepareImgFlg3.png",
                  "PrepareImgFlg4.png", "PrepareImgFlg5.png"]
BattleFieldItemHeight = 17


def make_regular_image(img, size=(256, 256)):
    return img.resize(size).convert('RGB')


def split_image(img, part_size=(64, 64)):
    w, h = img.size
    pw, ph = part_size

    assert w % pw == h % ph == 0

    return [img.crop((i, j, i + pw, j + ph)).copy() \
            for i in xrange(0, w, pw) \
            for j in xrange(0, h, ph)]


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def calc_similar(li, ri):
    li = make_regular_image(li)
    ri = make_regular_image(ri)
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):
    li, ri = make_regular_image(Image.open(lf)), make_regular_image(Image.open(rf))
    return calc_similar(li, ri)


def to_real_pos(pos):
    return int(float(pos) / SCREEN_SCALE)


def init_wow_window_pos():
    handle = win32gui.FindWindow("GxWindowClass", None)
    print "WOW window id = %s" % handle
    if handle == 0:
        print "Can not find Wow window!"
        return False
    else:
        win32gui.SetForegroundWindow(handle)
        win32gui.MoveWindow(handle, to_real_pos(0), to_real_pos(0), to_real_pos(2258), to_real_pos(1270), True)
        win32gui.SetForegroundWindow(handle)
        return True


def grab_join_dialog_img():
    img = ImageGrab.grab(JoinDialogBbox)
    return img


def grab_leave_dialog_img():
    img = ImageGrab.grab(LeaveDialogBbox)
    return img


def grab_escape_icon():
    img = ImageGrab.grab(EscapeIconBbox)
    return img


def grab_prepare_img(row):
    img = ImageGrab.grab(PrepareEnterBboxList[row])
    return img


if __name__ == '__main__':
    init_wow_window_pos()
    # grab_join_dialog_img().save(JoinImgName)
    # grab_leave_dialog_img().save(LeaveImgName)
    # grab_escape_icon().save(EscapeIconName)
    # grab_prepare_img(row).save(PrepareImgName[row])

    flag_img = []
    for i in range(0, 5):
        flag_img.append(Image.open(PrepareImgName[i]))

    while True:
        time.sleep(2)
        for i in range(0, 5):
            cur_image = grab_prepare_img(i)
            print calc_similar(cur_image, flag_img[i])
        print "***************"



























