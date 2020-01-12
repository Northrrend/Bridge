import logging
import time
import datetime
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

if __name__=='__main__':

    if not window.init_wow_window_pos():
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'Locate wow window failed exit'
        exit(-1)

    account.login()
    time.sleep(2)
    warrior = Role()
    warrior.change_chatframe()
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
    print dt_ms + 'Wait 1 seconds to start script'
    time.sleep(1)

    while True:
        warrior.join_bfqueue()
        time.sleep(BF_WaitingTime)
        if newbattle():
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'new battlefield enter now'
            warrior.enter_bf2()
            time.sleep(Reload_WaitingTime)
            warrior.all_a()
            warrior.jump(BF_PrepareTime)
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'march to bridges'
            t = warrior.to_bridge()
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'start defence'
            while t < BF_WinningTime :
                warrior.anti_afk()
                r = 30
                time.sleep(r)
                if endbattle():
                    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
                    print dt_ms + 'battle end'
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
