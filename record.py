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

time.sleep(4)
print 'record start'
m1 = KeyboardActionListener(file_name='keyboard.action')
m1.start()

