import logging
import time
from multiprocessing import Process
from multiprocessing import Pool
import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard
import random

global BF_WaitingTime, Logout_WaitingTime, Logout_WaitingTime, AFK_WaitingTime, BF_PrepareTime, Ave_WaitingTime

# BF_WaitingTime + BF_PrepareTime = 120
BF_WaitingTime = 10
BF_PrepareTime = 110
Logout_WaitingTime = 5
Login_WaitingTime = 10
AFK_WaitingTime = 10
Ave_WaitingTime = 900

global MountKey, NPCKey

TargetKey = 'g'
NPCKey = '.'
MountKey1 = 'g'
MountKey2 = 'q'


def battle_field(k):
    print 'Try to join battlefield'
    k.tap_key(TargetKey)
    time.sleep(0.1)
    k.tap_key(NPCKey)
    time.sleep(0.1)
    _button(k, 'GossipTitleButton1')
    time.sleep(0.1)
    _button(k, 'BattlefieldFrameJoinButton')
    time.sleep(0.1)
    print 'Wait ' + str(BF_WaitingTime) + ' to enter Battlefield'
    time.sleep(BF_WaitingTime)
    _button(k, 'StaticPopup1Button1')

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
    _button(k, 'WorldStateScoreFrameLeaveButton')

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
        r = random.randint(15, 20)
        time.sleep(r)
        c = c + r   
        print 'Defence end in ' + str(t - c) + ' s...'

def defence(k, t):
    c = 0
    while c < t :
        _anti_afk2(k)
        battle_field(k)
        #r = random.randint(70, 90)
        r = 50
        time.sleep(r)
        c = c + r + 10
        print 'Defence end in ' + str(t - c) + ' s...'


def to_bridge(k, i):
    print 'March to bridge'
    if i == 1:
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
    else:
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
    print 'Now get out of battlefield'
    _button(k, 'WorldStateScoreFrameLeaveButton')
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

def _anti_afk(k):
    k.tap_key(k.enter_key)
    time.sleep(0.1)
    k.type_string('/g')
    time.sleep(0.1)
    k.tap_key(k.space_key)
    time.sleep(0.1)
    k.type_string('usb')
    time.sleep(0.1)
    k.tap_key(k.enter_key)

def _anti_afk2(k):
    k.tap_key('6')

if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    i = 0  #initial role
    k = PyKeyboard()
    time.sleep(2)
    while True:
        battle_field(k)
        print 'Wait ' + str(BF_PrepareTime) + ' for battle to start'
        jump(k, BF_PrepareTime)
        to_bridge(k, i)
        defence(k, Ave_WaitingTime)
        afk(k)
        i = change_role(k, i)
        print i