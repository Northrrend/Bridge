import logging
import time
from multiprocessing import Process
from multiprocessing import Pool
import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard
import random
from capture import *
from role import Role
import window

global BF_WaitingTime, Logout_WaitingTime, Logout_WaitingTime, AFK_WaitingTime, BF_PrepareTime, Ave_WaitingTime

BF_WaitingTime = 5
BF_PrepareTime = 110
Logout_WaitingTime = 5
Login_WaitingTime = 10
AFK_WaitingTime = 10
BF_WinningTime = 60*40
Reload_WaitingTime = 5
Escape_WaitingTime = 60*15

global MountKey, NPCKey

TargetKey = 'g'
NPCKey = '.'
MountKey1 = 'g'
MountKey2 = 'q'


def join_bf(k):
    k.tap_key(TargetKey)
    time.sleep(0.1)
    k.tap_key(NPCKey)
    time.sleep(0.1)
    _button(k, 'GossipTitleButton1')
    time.sleep(0.1)
    _button(k, 'BattlefieldFrameJoinButton')

def enter_bf(k):
    _button(k, 'StaticPopup1Button1')

def cancel_bf(k):
    _button(k, 'DropDownList1Button3')

def cancel_bf2(k):
    _button_right(k, 'MiniMapBattlefieldFrame')
    _button(k, 'DropDownList1Button3')

def quit_bf(k):
    _button(k, 'WorldStateScoreFrameLeaveButton')

def change_role(k, i):
    print 'Change to another role'
    if i == 0:
        i = 1
        key = k.down_key
    else:
        i = 0 
        key = k.up_key
    k.tap_key(k.enter_key)
    time.sleep(0.1)
    k.type_string('/logout')
    time.sleep(0.1)
    k.tap_key(k.enter_key)
    time.sleep(0.1)
    time.sleep(Logout_WaitingTime)
    k.tap_key(key)
    time.sleep(0.1)
    k.tap_key(k.enter_key)
    time.sleep(Login_WaitingTime)
    return i

def march(k, t):
    k.press_key('w')
    time.sleep(t)
    k.release_key('w')

def turn_right(k, t):
    k.press_key(k.right_key)
    time.sleep(t)
    k.release_key(k.right_key)

def mount(k):
    k.press_key(k.alt_key)
    k.tap_key(MountKey1)
    k.release_key(k.alt_key)
    time.sleep(3)

def mount2(k):
    k.tap_key(MountKey2)
    time.sleep(3)

def jump(k, t):
    c = 0
    while c < t :
        k.tap_key(k.space_key)
        r = random.randint(35, 55)
        time.sleep(r)
        c = c + r   
        print 'Jump end in ' + str(t - c) + ' s...'

def defence(k, t):
    c = 0
    while c < t :
        _anti_afk2(k)
        r = 30
        time.sleep(r)
        if endbattle():
            print 'battle is end ...'
            quit_bf(k)
            time.sleep(Reload_WaitingTime)
            return 'end'
        c = c + r
        print 'Defence end in ' + str(t - c) + ' s...'
    afk(k)
    time.sleep(Escape_WaitingTime)


def to_bridge(k):
    march(k, 2)
    time.sleep(0.1)
    turn_right(k, 0.28)
    march(k, 14)
    time.sleep(0.2)
    mount(k)
    turn_right(k, 0.1)
    march(k, 4)
    turn_right(k, 0.28)
    march(k, 18)
    turn_right(k, 0.8)
    march(k, 10)
    mount(k)

def to_bridge_small(k):
    march(k, 2)
    time.sleep(0.1)
    turn_right(k, 0.28)
    march(k, 14)
    time.sleep(0.2)
    mount(k)
    turn_right(k, 0.1)
    march(k, 7)
    turn_right(k, 0.3)
    march(k, 15)
    turn_right(k, 0.1)
    march(k, 15)
    mount(k)

def afk(k):
    print 'Timeout get out of battlefield'
    k.tap_key(k.enter_key)
    time.sleep(0.1)
    k.type_string('/afk')
    time.sleep(0.1)
    k.tap_key(k.enter_key)
    time.sleep(AFK_WaitingTime)

def _button(k, s):
    k.tap_key(k.enter_key)
    time.sleep(0.1)
    k.type_string('/click')
    time.sleep(0.1)
    k.tap_key(k.space_key)
    time.sleep(0.1)
    k.type_string(s)
    time.sleep(0.1)
    k.tap_key(k.enter_key)

def _button_right(k, s):
    k.tap_key(k.enter_key)
    time.sleep(0.1)
    k.type_string('/click')
    time.sleep(0.1)
    k.tap_key(k.space_key)
    time.sleep(0.1)
    k.type_string(s)
    time.sleep(0.1)
    k.tap_key(k.space_key)
    k.type_string('RightButton')
    k.tap_key(k.enter_key)

def _anti_afk2(k):
    k.tap_key('6')

if __name__=='__main__':

    if not window.init_wow_window_pos():
        print('Locate wow window failed exit')
        exit(-1)
    
    warrior = Role()
    k = PyKeyboard()
    print 'Wait 2 seconds to start script'
    time.sleep(2)

    while True:
        warrior.join_bfqueue()
        time.sleep(BF_WaitingTime)
        if newbattle():
            print 'new battlefield enter now'
            warrior.enter_bf()
            warrior.jump(BF_PrepareTime)
            print 'march to bridges'
            to_bridge(k)
            print 'start defence'
            c = 0
            while c < BF_WinningTime :
                warrior.anti_afk()
                r = 30
                time.sleep(r)
                if endbattle():
                    print 'battle end'
                    warrior.quit_bf()
                    time.sleep(Reload_WaitingTime)
                    break
                c = c + r
                print 'Defence end in ' + str(BF_WaitingTime - c) + ' s...'
            warrior.quit_bf_afk()
            time.sleep(Escape_WaitingTime)
        else:
            warrior.leave_bfqueue()
            time.sleep(0.3)

    #i = 0 
    #k = PyKeyboard()
    #while True:
    #    join_bf
    #    print 'Wait ' + str(BF_PrepareTime) + ' for battle to start'
    #    jump(k, BF_PrepareTime)
    #    to_bridge(k, i)
    #    defence(k, Ave_WaitingTime)
    #    afk(k)
    #    i = change_role(k, i)
    #    pr
    #    int i
    
    
    #k = PyKeyboard()
    #while True:
    #    join_bf(k)
    #    time.sleep(BF_WaitingTime)
    #    if newbattle():
    #        enter_bf(k)
    #        print 'enter battle ...'
    #        jump(k, BF_PrepareTime)
    #        print 'march to bridges'
    #        to_bridge(k)
    #        print 'start defence'
    #        defence(k, BF_WinningTime)
    #    else:
    #        cancel_bf2(k)
    #        time.sleep(0.3)