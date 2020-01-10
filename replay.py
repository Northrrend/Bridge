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
                        time.sleep(0.04)

                    elif obj['event'] == 'release':
                        keyboard_exec.release(KeyCode.from_vk(obj['vk']))
                        time.sleep(0.01)
                line = file.readline()

class KeyboardActionListener(threading.Thread):

    def __init__(self, file_name):
        super(KeyboardActionListener, self).__init__()
        self.file_name = file_name

    def run(self):
        with open(self.file_name, 'w') as file:
            def on_press(key):
                template = keyboard_action_template()
                template['event'] = 'press'
                try:
                    template['vk'] = key.vk
                except AttributeError:
                    template['vk'] = key.value.vk
                finally:
                    file.writelines(json.dumps(template) + "\n")
                    file.flush()

            def on_release(key):
                if key == keyboard.Key.esc:
                    return False
                template = keyboard_action_template()
                template['event'] = 'release'
                try:
                    template['vk'] = key.vk
                except AttributeError:
                    template['vk'] = key.value.vk
                finally:
                    file.writelines(json.dumps(template) + "\n")
                    file.flush()

            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()


def action(filename):

    m2 = KeyboardActionExecute(file_name=filename)
    m2.start()

time.sleep(4)
print 'record start'
m1 = KeyboardActionListener(file_name='keyboard.action')
m1.start()