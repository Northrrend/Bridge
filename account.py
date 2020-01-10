import logging
import time
import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard
import random

def login():
    username = ''
    password = ''
    k = PyKeyboard()
    k.type_string(username)
    time.sleep(0.1)
    k.tap_key(k.tab_key)
    time.sleep(0.1)
    k.type_string(password)
    time.sleep(0.1)
    k.tap_key(k.enter_key)
    time.sleep(5)
    k.tap_key(k.enter_key)
    time.sleep(10)
    k.tap_key(k.enter_key)
    time.sleep(5)
