import json
import threading
import time

from pynput import keyboard
from pynput.keyboard import Controller, KeyCode


def keyboard_action_template():
    return {
        "name": "keyboard",
        "event": "default",
        "vk": "default"
    }

class KeyboardActionExecute(threading.Thread):

    def __init__(self, file_name):
        super(KeyboardActionExecute, self).__init__()
        self.file_name = file_name

    def run(self):
        with open(self.file_name, 'r') as file:
            keyboard_exec = Controller()
            line = file.readline()
            time.sleep(3)
            while line:
                obj = json.loads(line)
                if obj['name'] == 'keyboard':
                    if obj['event'] == 'press':
                        keyboard_exec.press(KeyCode.from_vk(obj['vk']))
                        time.sleep(0.01)

                    elif obj['event'] == 'release':
                        keyboard_exec.release(KeyCode.from_vk(obj['vk']))
                        time.sleep(0.01)
                line = file.readline()


def action(filename):

    m2 = KeyboardActionExecute(file_name=filename)
    m2.start()