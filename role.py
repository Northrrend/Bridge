import logging
import time
import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard
import random

class Role(object):

    def __init__(self):
        self.k = PyKeyboard()
        self.TargetKey = ','
        self.NPCKey = '.'
        self.MountKey1 = 'g'
        self.MountKey2 = 'q'
        self.AntiAFKKey = '6'

    def join_bfqueue(self):
        self.k.tap_key(self.TargetKey)
        time.sleep(0.1)
        self.k.tap_key(self.NPCKey)
        time.sleep(0.1)
        self._left_click('GossipTitleButton1')
        time.sleep(0.1)
        self._left_click('BattlefieldFrameJoinButton')

    def leave_bfqueue(self):
        self._right_click('MiniMapBattlefieldFrame')
        self._left_click('DropDownList1Button3')
    
    def enter_bf(self):
        self._left_click('StaticPopup1Button1')

    def quit_bf(self):
        self._left_click('WorldStateScoreFrameLeaveButton')
    
    def quit_bf_afk(self):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        self.k.type_string('/afk')
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
    
    def mount(self):
        self.k.press_key(self.k.alt_key)
        self.k.tap_key(self.MountKey1)
        self.k.release_key(self.k.alt_key)
        time.sleep(3)
    
    def jump(self, t):
        c = 0
        while c < t :
            self.k.tap_key(self.k.space_key)
            r = random.randint(35, 55)
            time.sleep(r)
            c = c + r   
    def change_chatframe(self):
        self._left_click('ChatFrame4Tab')

    def anti_afk(self):
        self.k.tap_key(self.AntiAFKKey)
    
    def all_a(self):
        self.k.tap_key('RaidFrameAllAssistCheckButton')
    
    def _left_click(self, s):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        self.k.type_string('/click')
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.1)
        self.k.type_string(s)
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)

    def _right_click(self, s):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        self.k.type_string('/click')
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.1)
        self.k.type_string(s)
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        self.k.type_string('RightButton')
        self.k.tap_key(self.k.enter_key)