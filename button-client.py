from pynput import keyboard
from ntcore import *

ntinstance = NetworkTableInstance.getDefault()
import sysconfig; print(sysconfig.get_path("scripts"))
ntinstance.startClient4('button-client')
ntinstance.setServerTeam(5826)

buttons = []

with open('button-client.ini') as f:
    buttons = [x.lstrip('0123456789').strip(':\n') for x in f.readlines()]

print('Current buttons: ',buttons)

button_dict = {}
for i in range(len(buttons)):
    button_dict[buttons[i]] = [ntinstance.getBooleanTopic('buttons/'+str(i)).publish(),False]

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char
    except:
        k = key.name
    if button_dict.get(k) != None:
        p = button_dict.get(k)[0]
        last_value = button_dict.get(k)[1]
        if not last_value:
            button_dict.get(k)[1] = True
            p.set(True)
            print(p.getTopic().getName())

def on_release(key):
    try:
        k = key.char
    except:
        k = key.name
    if button_dict.get(k) != None:
        last_value = button_dict.get(k)[1]
        p = button_dict.get(k)[0]
        if p != None and last_value:
            button_dict.get(k)[1] = False
            p.set(False)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()