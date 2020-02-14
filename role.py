import logging
import time
import pymouse,pykeyboard,os,sys
from pykeyboard import PyKeyboard
import random
import KeymouseGo

class Role(object):

    def __init__(self):
        self.k = PyKeyboard()
        self.TargetKey = ','
        self.NPCKey = '.'
        self.MountKey1 = 'g'
        self.AntiAFKKey = '6'
        self.TargetKey2 = '\''
        self.index = 0
    
    def reload(self):
        self.k.type_string('/reload')
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)

    def _left_click(self, s):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.3)
        self.k.type_string('/click')
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.1)
        self.k.type_string(s)
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)

    def _right_click(self, s):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.3)
        self.k.type_string('/click')
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.1)
        self.k.type_string(s)
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.1)
        self.k.type_string('RightButton')
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)

    def join_bfqueue(self):
        #This is used to prevent bad guy to summon you
        self._left_click('StaticPopup1Button2')
        self.k.tap_key(self.TargetKey)
        time.sleep(0.3)
        self.k.tap_key(self.NPCKey)
        time.sleep(0.3)
        self._left_click('GossipTitleButton1')
        time.sleep(0.3)
        self._left_click('BattlefieldFrameJoinButton')
        time.sleep(0.1)

    def leave_bfqueue(self):
        self._right_click('MiniMapBattlefieldFrame')
        self._left_click('DropDownList1Button3')

    def enter_bf(self):
        self._right_click('MiniMapBattlefieldFrame')
        time.sleep(0.3)
        self._left_click('DropDownList1Button2')

    def quit_bf(self):
        self._left_click('WorldStateScoreFrameLeaveButton')
    
    def quit_bf2(self):
        self._left_click('WorldStateScoreFrameLeaveButton')
        time.sleep(0.3)
        self._left_click('StaticPopup1Button1')
    
    def quit_bf_afk(self):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        self.k.type_string('/afk')
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
    
    def mount(self):
        self.k.press_key(self.k.alt_key)
        self.k.tap_key(self.MountKey1)
        self.k.release_key(self.k.alt_key)
        time.sleep(4)
        return 4
    
    def jump(self, t):
        c = 0
        while c < t :
            self.k.tap_key(self.k.space_key)
            r = random.randint(35, 55)
            time.sleep(r)
            c = c + r   
        return c

    def change_chatframe(self):
        self._left_click('ChatFrame4Tab')

    def anti_afk(self):
        self.k.tap_key(self.AntiAFKKey)
    
    def all_a(self):
        self._left_click('RaidFrameAllAssistCheckButton')
    
    def to_bridge(self):
        self.march(2)
        time.sleep(0.1)
        self.turn_right(0.28)
        self.march(14)
        time.sleep(0.2)
        self.mount()
        self.turn_right(0.1)
        self.march(4)
        self.turn_right(0.28)
        self.march(18)
        self.turn_right(0.8)
        self.march(10)
        self.mount()
        return 52

    def donate(self):
        self.k.tap_key(self.TargetKey2)
        time.sleep(0.3)
        self.k.tap_key(self.NPCKey)
        time.sleep(0.3)
        self._left_click('GossipTitleButton1')
        time.sleep(0.3)
        self._left_click('QuestFrameCompleteButton')
        time.sleep(0.3)
        self._left_click('QuestFrameCompleteQuestButton')
        time.sleep(0.3)
        self._left_click('GossipFrameGreetingGoodbyeButton')
        time.sleep(0.3)
        self._left_click('GossipFrameGreetingGoodbyeButton')
        time.sleep(0.1)

    def gtalk(self):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        self.k.type_string('/g')
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.1)
        self.k.type_string('There stands the iron armor!!!')
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
    
    def ptalk(self, s):
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        self.k.type_string('/p')
        time.sleep(0.1)
        self.k.tap_key(self.k.space_key)
        time.sleep(0.1)
        self.k.type_string(s)
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
    
    def ready(self):
        self.ptalk('MPP')
    
    def report_new(self):
        self.ptalk('MPO')

    def report_old(self):
        self.ptalk('OLD')

    def test_action(self):
        filename = 'to_gate.txt'
        t = KeymouseGo.single_run(filename)
        return t
    
    def march(self, t):
        self.k.press_key('w')
        time.sleep(t)
        self.k.release_key('w')
    
    def turn_right(self, t):
        self.k.press_key(self.k.right_key)
        time.sleep(t)
        self.k.release_key(self.k.right_key)
    
    def change_role(self):
        if self.index == 0:
            self.index = 1
            key = self.k.down_key
        else:
            self.index = 0 
            key = self.k.up_key
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        self.k.type_string('/logout')
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(0.1)
        time.sleep(10)
        self.k.tap_key(key)
        time.sleep(0.1)
        self.k.tap_key(self.k.enter_key)
        time.sleep(10)
    
    def ready_check(self):
        self._left_click('ReadyCheckFrameYesButton')

