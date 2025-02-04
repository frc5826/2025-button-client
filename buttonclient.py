from pynput import keyboard
from ntcore import *

ntinstance = NetworkTableInstance.getDefault()

ntinstance.startClient4('button-client')
ntinstance.setServerTeam(5826)

buttons = ['a','b','c']
button_dict = {}
for i in range(len(buttons)):
    button_dict[buttons[i]] = ntinstance.getBooleanTopic('buttons/'+str(i)).publish()

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char
    except:
        k = key.name
    p = button_dict.get(k)
    if p != None:
        p.set(True)
        print(p.getTopic().getName())

def on_release(key):
    try:
        k = key.char
    except:
        k = key.name
    p = button_dict.get(k)
    if p != None:
        p.set(True)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()