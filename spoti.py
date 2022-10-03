from AppOpener import run
import time
import pyautogui
run("spotify")
time.sleep(5)
pyautogui.hotkey('ctrl', 'l')
time.sleep(2)
pyautogui.write("Aurora", interval=0.1)
time.sleep(2)
for key in ['enter', 'tab', 'enter', 'enter']:
    time.sleep(1)
    pyautogui.press(key)
