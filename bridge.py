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
import account


BF_WaitingTime = 5
BF_PrepareTime = 110
Logout_WaitingTime = 5
Login_WaitingTime = 10
AFK_WaitingTime = 10
BF_WinningTime = 60*40
Reload_WaitingTime = 5
Escape_WaitingTime = 60*15

MountKey1 = 'g'
MountKey2 = 'q'

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

if __name__=='__main__':

    if not window.init_wow_window_pos():
        print('Locate wow window failed exit')
        exit(-1)

    account.login()
    time.sleep(2)
    warrior = Role()
    warrior.change_chatframe()
    k = PyKeyboard()
    print 'Wait 1 seconds to start script'
    time.sleep(1)

    while True:
        warrior.join_bfqueue()
        time.sleep(BF_WaitingTime)
        if newbattle():
            print 'new battlefield enter now'
            warrior.enter_bf()
            time.sleep(Reload_WaitingTime)
            warrior.all_a()
            warrior.jump(BF_PrepareTime)
            print 'march to bridges'
            to_bridge(k)
            print 'start defence'
            t = 0
            while t < BF_WinningTime :
                warrior.anti_afk()
                r = 30
                time.sleep(r)
                if endbattle():
                    print 'battle end'
                    warrior.quit_bf()
                    time.sleep(Reload_WaitingTime)
                    break
                t = t + r
                print 'Defence end in ' + str(BF_WinningTime - t) + ' s...'
            if t >= BF_WinningTime :
                warrior.quit_bf_afk()
                #time.sleep(Reload_WaitingTime)
                time.sleep(Escape_WaitingTime)
        else:
            print 'old leave'
            warrior.leave_bfqueue()
            time.sleep(0.3)
