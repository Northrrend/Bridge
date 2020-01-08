import time
import os,sys
from pymouse import *
from pykeyboard import PyKeyboard
import random
import utils
from PIL import Image


# BF_WaitingTime = 10
BF_PrepareTime = 115
# Logout_WaitingTime = 5
# Login_WaitingTime = 10
# AFK_WaitingTime = 10
# Ave_WaitingTime = 900


# def change_role(k, i):
#     if i == 0:
#         i = 1
#         key = k.down_key
#     else:
#         i = 0
#         key = k.up_key
#     k.tap_key(k.enter_key)
#     time.sleep(0.1)
#     k.type_string('/logout')
#     time.sleep(0.1)
#     k.tap_key(k.enter_key)
#     time.sleep(0.1)
#     time.sleep(Logout_WaitingTime)
#     k.tap_key(key)
#     time.sleep(0.1)
#     k.tap_key(k.enter_key)
#     time.sleep(Login_WaitingTime)
#     return i


# def to_bridge(k, i):
#     if i == 1:
#         march(k, 2)
#         time.sleep(0.1)
#         turn_right(k, 0.28)
#         march(k, 14)
#         time.sleep(0.2)
#         mount(k)
#         turn_right(k, 0.1)
#         march(k, 4)
#         turn_right(k, 0.3)
#         march(k, 18)
#         turn_right(k, 1)
#         march(k, 10)
#         mount(k)
#     else:
#         march(k, 2)
#         time.sleep(0.1)
#         turn_right(k, 0.28)
#         march(k, 14)
#         time.sleep(0.2)
#         mount(k)
#         turn_right(k, 0.1)
#         march(k, 7)
#         turn_right(k, 0.3)
#         march(k, 15)
#         turn_right(k, 0.1)
#         march(k, 15)
#         mount(k)


def sec_to_time(seconds):
    if seconds <= 60:
        return str(seconds) + " s"
    else:
        m = int(seconds / 60)
        s = seconds % 60
        return "%sm %ss" % (m, s)


class AutoAlterac:
    k = PyKeyboard()
    m = PyMouse()
    JoinImgFlg = Image.open("JoinImgFlg.png")
    LeaveImgFlg = Image.open("LeaveImgFlg.png")
    EscapeIcon = Image.open("EscapeIcon.png")
    PrepareImgFlg = []

    BATTLE_FINISHED = 0
    BATTLE_ESCAPED = 1

    fieldNum = 0

    def __init__(self):
        for i in range(0, 5):
            self.PrepareImgFlg.append(Image.open(utils.PrepareImgName[i]))

    def battle_field(self):
        while True:
            self.__target_npc()
            time.sleep(0.2)
            self.__interact_npc()
            time.sleep(0.2)
            self.__queue_for_battle()
            time.sleep(0.2)
            t = self.__wait_to_join(120)
            if t >= 0:
                if self.__check_new_field():
                    print "Prepare to join battle field...."
                    for i in range(3, 0, -1):
                        print i
                        time.sleep(1)
                    self.__join_to_battle()
                    return t
                else:
                    print "No new field! Reset!"
                    self.__leave_battle_queue()
            else:
                self.__leave_battle_queue(1)
                continue

    def __leave_battle_queue(self, t=0):
        print "start leave battle queue!"
        time.sleep(1)
        self.__mouse_click(1978, 230, 2)
        time.sleep(1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(1)
        if t == 0:
            self.__mouse_click(2021, 314)
        else:
            self.__mouse_click(2021, 295)
        time.sleep(1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(1)
        print "leave!"

    def to_bridge(self, wait_time):
        self.march(2)
        time.sleep(0.1)
        self.turn_right(0.28)
        self.march(8.5)
        time.sleep(wait_time)
        self.march(5.5)
        time.sleep(0.2)
        self.mount()
        self.turn_right(0.1)
        self.march(5.6)
        self.turn_right(0.3)
        self.march(12)
        self.turn_right(0.1)
        self.march(12)
        self.mount()
        self.k.tap_key(self.k.function_keys[4])
        time.sleep(2)

    def defence(self, t):
        c = 0
        while True:
            self.__speak("For the alliance!")
            r = random.randint(10, 20)
            time.sleep(r)
            c = c + r
            print 'Field %s:Defence %s' % (self.fieldNum, sec_to_time(c))
            if self.check_battle_finish():
                print "Battle finished!"
                self.__leave_battle()
                time.sleep(30)
                return self.BATTLE_FINISHED
            if self.check_escape():
                print "Battle escaped!"
                return self.BATTLE_ESCAPED
            if c > t:
                print "Battle timeout , AFK!"
                self.__afk()
                time.sleep(30)
                return self.BATTLE_ESCAPED

    def away_from_kbd(self, t):
        c = 0
        while c < t:
            self.k.tap_key(self.k.space_key)
            r = random.randint(10, 20)
            time.sleep(r)
            c = c + r
            print "rest:" + sec_to_time(t - c) + " left"

    def march(self, t):
        self.k.press_key('w')
        time.sleep(t)
        self.k.release_key('w')

    def turn_right(self, t):
        self.k.press_key(self.k.right_key)
        time.sleep(t)
        self.k.release_key(self.k.right_key)

    def mount(self):
        self.k.press_key(self.k.alt_key)
        self.k.tap_key('t')
        self.k.release_key(self.k.alt_key)
        time.sleep(3.5)

    def check_battle_finish(self):
        cur_img = utils.grab_leave_dialog_img()
        sim = utils.calc_similar(cur_img, self.LeaveImgFlg)
        if sim > 0.95:
            return True
        else:
            return False

    def check_escape(self):
        cur_img = utils.grab_escape_icon()
        sim = utils.calc_similar(cur_img, self.EscapeIcon)
        if sim > 0.95:
            return True
        else:
            return False

    def __target_npc(self):
        self.k.tap_key('9')
        print "Target NPC"

    def __interact_npc(self):
        self.k.tap_key('0')
        print "interact"

    def __queue_for_battle(self):
        self.__click_macro('GossipTitleButton1')
        # for i in range(0, 30):
        #     self.__mouse_click(386, 436)
        #     time.sleep(0.1)
        # time.sleep(1)
        # self.__mouse_click(196, 454)
        # time.sleep(1)
        time.sleep(0.2)
        self.__click_macro('BattlefieldFrameJoinButton')

    def __check_new_field(self):
        self.__target_npc()
        time.sleep(0.2)
        self.__interact_npc()
        time.sleep(0.2)
        self.__click_macro('GossipTitleButton1')
        time.sleep(0.2)
        for i in range(0, 30):
            self.__mouse_click(386, 436)
            time.sleep(0.1)
        print "Check new field...."
        for i in range(0, 5):
            cur_image = utils.grab_prepare_img(i)
            sim = utils.calc_similar(cur_image, self.PrepareImgFlg[i])
            print i, sim
            if sim > 0.95:
                return True
        return False

    def __wait_to_join(self, limit):
        t = 0
        while True:
            if t > limit:
                return -1
            print "wait ti join...."
            time.sleep(2)
            t = t + 2
            cur_img = utils.grab_join_dialog_img()
            sim = utils.calc_similar(cur_img, self.JoinImgFlg)
            print sim
            if sim > 0.8:
                return t

    def __join_to_battle(self):
        self.__click_macro('StaticPopup1Button1')
        self.fieldNum += 1
        print "Join battle field!"

    def __afk(self):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.2)
        self.k.type_string('/afk')
        time.sleep(0.2)
        self.k.tap_key(self.k.enter_key)

    def __leave_battle(self):
        print "Leave battle!"
        self.__click_macro('WorldStateScoreFrameLeaveButton')

    def __click_macro(self, s):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.2)
        self.k.type_string('/click')
        time.sleep(0.2)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.2)
        self.k.type_string(s)
        time.sleep(0.2)
        self.k.tap_key(self.k.enter_key)

    def __speak(self, s):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.2)
        self.k.type_string('/5')
        time.sleep(0.2)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.2)
        self.k.type_string(s)
        time.sleep(0.2)
        self.k.tap_key(self.k.enter_key)

    def __mouse_click(self, x, y, btn=1):
        self.m.click(utils.to_real_pos(x), utils.to_real_pos(y), btn)

    def __mouse_move(self, x, y):
        self.m.move(utils.to_real_pos(x), utils.to_real_pos(y))


if __name__ == '__main__':
    if not utils.init_wow_window_pos():
        exit(-1)
    auto_as = AutoAlterac()
    time.sleep(2)

    # auto_as.to_bridge(0.1)
    # exit(0)

    a = 1

    while True:
        if not a == 0:
            wt = auto_as.battle_field()
            time.sleep(30)
            p_time = BF_PrepareTime - 30
            print "Wait %s s to prepare...." % p_time
            # time.sleep(p_time)
            auto_as.to_bridge(p_time)
        a = 1
        state = auto_as.defence(2400)
        if state == AutoAlterac.BATTLE_FINISHED:
            continue
        elif state == AutoAlterac.BATTLE_ESCAPED:
            auto_as.away_from_kbd(900)
            continue



