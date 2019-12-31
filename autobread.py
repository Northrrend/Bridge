import logging
import time
from multiprocessing import Process
from multiprocessing import Pool
import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard

global WaterBtn, BreadBtn, ItemBtn, TradeBtn, CancelBtn, DrinkBtn, PrBtn

WaterBtn = '2'
BreadBtn = '1'
ItemBtn = '4'
TradeBtn = '5'
CancelBtn = '6'
DrinkBtn ='8'
PrBtn = '3'
BagBtn = 'b'
MakeBtn = '7'

def trade(k):
    try:
        while True:
            print('add item')
            k.tap_key(ItemBtn)
            time.sleep(0.2)
            print('trade button')
            k.tap_key(TradeBtn)
            time.sleep(3)
            #print('cancel button')
    except KeyboardInterrupt,e:
        print "you stop the threading"

def cook(k):
    try:
        while True:
            print('jump')
            k.tap_key(k.space_key)
            time.sleep(0.1)
            print('cook water')
            k.tap_key(WaterBtn)
            time.sleep(3.1)
            print('cook water')
            k.tap_key(WaterBtn)
            time.sleep(3.1)
            print('cook water')
            k.tap_key(WaterBtn)
            time.sleep(3.1)
            print('cook water')
            k.tap_key(WaterBtn)
            time.sleep(3.1)
            print('cook water')
            k.tap_key(WaterBtn)
            time.sleep(3.1)
            print('cook water')
            k.tap_key(WaterBtn)
            time.sleep(3.1)
            print('cook bread')
            k.tap_key(BreadBtn)
            time.sleep(3.1)
            print('cook bread')
            k.tap_key(BreadBtn)
            time.sleep(3.1)
            print('drink water')
            k.tap_key(DrinkBtn)
            time.sleep(30)
    except KeyboardInterrupt,e:
        print "you stop the threading"

def pr(k): 
    try:
        while True:
            print('open bag')
            k.tap_key(BagBtn)
            print('bag order')
            k.tap_key(MakeBtn)
            print('pr')
            k.tap_key(PrBtn)
            time.sleep(120)
    except KeyboardInterrupt,e:
        print "you stop the threading"


if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()

    time.sleep(5)
    m = PyMouse()
    k = PyKeyboard()
    p = Pool()
    p.apply_async(trade,args=(k,))
    p.apply_async(cook,args=(k,))
    p.apply_async(pr,args=(k,))
    p.close()
    p.join()
     