import logging
import time
import datetime
from multiprocessing import Process
from multiprocessing import Pool
import pymouse,pykeyboard,os,sys
import random
from role import Role
import account
from capture import Eye


BF_WaitingTime = 5
BF_PrepareTime = 110
BF_WinningTime = 60*40
Reload_WaitingTime = 7
Escape_WaitingTime = 60*15
code_list = ["MMO","OLD","BTO","MPO","TKB"]
#MMO ... new BF
#OLD ... old BF
#BTO ... BF pop up
#MPO ... slave ready
#TKB ... BF end

def classic():
    while True:
        warrior.join_bfqueue()
        code = 'NULL'
        while code <> 'BTO':
            time.sleep(15)
            code = eye.dashboard(code_list)

        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'new battlefield enter now'
        warrior.enter_bf()
        time.sleep(Reload_WaitingTime)
        warrior.all_a()
        warrior.jump(BF_PrepareTime)
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'march to bridges'
        t = warrior.to_bridge()
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'start defence'
        while t < BF_WinningTime :
            print 'Defence end in ' + str(BF_WinningTime - t) + ' s...'
            warrior.anti_afk()
            r = 30
            time.sleep(r)
            code = eye.dashboard(code_list)
            if code == "TKB":
                dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
                print dt_ms + 'battle end'
                warrior.quit_bf()
                time.sleep(Reload_WaitingTime)
                #for virtual machine
                time.sleep(Reload_WaitingTime)
                warrior.donate()
                break
            if code == "MPP":
                t = BF_WinningTime
            t = t + r
        if t >= BF_WinningTime :
            warrior.quit_bf_afk()
            time.sleep(Escape_WaitingTime)

def master():
    while True:
        code = 'NULL'
        while code <> 'MPP':
            time.sleep(5)
            code = eye.dashboard(code_list)
        warrior.join_bfqueue_group()
        while code <> 'BTO':
            time.sleep(5)
            code = eye.dashboard(code_list)
        time.sleep(20)
        code = eye.dashboard(code_list)
        if code == 'MMO':
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'new battlefield enter now'
            warrior.enter_bf()
            time.sleep(Reload_WaitingTime)
            warrior.all_a()
            warrior.jump(BF_PrepareTime)
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'march to bridges'
            t = warrior.to_bridge()
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'start defence'
            while t < BF_WinningTime :
                print 'Defence end in ' + str(BF_WinningTime - t) + ' s...'
                warrior.anti_afk()
                r = 30
                time.sleep(r)
                code = eye.dashboard(code_list)
                if code == "TKB":
                    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
                    print dt_ms + 'battle end'
                    warrior.quit_bf()
                    time.sleep(Reload_WaitingTime)
                    #for virtual machine
                    time.sleep(Reload_WaitingTime)
                    warrior.donate()
                    break
                t = t + r
            if t >= BF_WinningTime :
                warrior.quit_bf_afk()
                time.sleep(Escape_WaitingTime)
        else:
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'old battlefield leave'
            warrior.leave_bfqueue()
            time.sleep(0.3)

def slave():
    code = 'NULL'
    while True:
        warrior.ready()
        while code <> 'BTO':
            time.sleep(15)
            code = eye.dashboard(code_list)
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'new battlefield enter now'
        warrior.enter_bf()
        time.sleep(Reload_WaitingTime)
        warrior.reload()
        time.sleep(Reload_WaitingTime)
        code = eye.dashboard(code_list)
        if code == 'MMO':
            warrior.jump(BF_PrepareTime)
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'march to bridges'
            t = warrior.to_bridge()
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
            print dt_ms + 'start defence'
            while t < BF_WinningTime :
                print 'Defence end in ' + str(BF_WinningTime - t) + ' s...'
                warrior.anti_afk()
                r = 30
                time.sleep(r)
                code = eye.dashboard(code_list)
                if code == "TKB":
                    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
                    print dt_ms + 'battle end'
                    warrior.quit_bf()
                    time.sleep(Reload_WaitingTime)
                    warrior.donate()
                    break
                t = t + r
            if t >= BF_WinningTime :
                warrior.quit_bf_afk()
                time.sleep(Escape_WaitingTime)
        else:
            warrior.quit_bf_afk()
            warrior.change_role()

def ws():
    while True:
        #warrior.join_bfqueue()
        code = 'NULL'
        while code <> 'BTO':
            time.sleep(5)
            warrior.ready_check()
            code = eye.dashboard(code_list)
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'new battlefield enter now'
        warrior.enter_bf()
        time.sleep(Reload_WaitingTime)
        warrior.jump(BF_PrepareTime)
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'march to cave'
        #t = warrior.to_bridge()
        while code <> 'TKB' :
            time.sleep(15)
            warrior.anti_afk()
            code = eye.dashboard(code_list)
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'battle end'
        warrior.quit_bf()
        time.sleep(Reload_WaitingTime)
        #warrior.march(5)
        #warrior.donate()

if __name__=='__main__':

    #1: master
    #2: slave
    #3: solo
    #4: jump
    #5: ws
    role = 4

    if role == 1:
        eye = Eye()
        #account.login()
        warrior = Role()
        warrior.gtalk()
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'Wait 1 seconds to start script'
        time.sleep(1)
        master()
    if role == 2:
        eye = Eye()
        #account.login()
        warrior = Role()
        warrior.gtalk()
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'Wait 1 seconds to start script'
        time.sleep(1)
        slave()
    if role == 3:
        eye = Eye()
        #account.login()
        warrior = Role()
        warrior.gtalk()
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'Wait 1 seconds to start script'
        time.sleep(1)
        classic()
    if role == 4:
        warrior = Role()
        while True:
            warrior.anti_afk()
            time.sleep(30)
    if role == 5:
        warrior = Role()
        warrior.gtalk()
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ')
        print dt_ms + 'Wait 1 seconds to start script'
        time.sleep(1)
        ws()
