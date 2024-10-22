import win32gui
import pyautogui
import threading
import time
import pyperclip
import keyboard
import win32con
from pynput import mouse

event = threading.Event()
windows = []
def get_window_callback(hwnd, windows):
    title = win32gui.GetWindowText(hwnd)
    if title:
        windows.append((hwnd, title))
def get_relative_pos(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x_abs, y_abs, _, _ = rect
    x_mouse, y_mouse = pyautogui.position()
    return x_mouse - x_abs, y_mouse - y_abs 
def move_to_relative_pos(hwnd, rx, ry):
    rect = win32gui.GetWindowRect(hwnd)
    x_abs, y_abs, _, _ = rect
    pyautogui.moveTo(x=x_abs+rx,y=y_abs+ry)
def on_click(x, y, button, pressed):
    if pressed:
        event.set()
def keep_foreground(hwnd):
    if hwnd:
        win32gui.ShowWindow(hwnd,win32con.SW_SHOWNORMAL)
        win32gui.SetForegroundWindow(hwnd)

def launch(hwnd, text_rx, text_ry, chat_rx, chat_ry, button_rx, button_ry):
    last_text = ''
    while True:
        if keyboard.is_pressed('esc'):
            break
        keep_foreground(hwnd)
        move_to_relative_pos(hwnd, chat_rx, chat_ry)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        text = pyperclip.paste()
        #print(text)
        if text != last_text:
            last_text = text
            move_to_relative_pos(hwnd, text_rx, text_ry)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'v')
            move_to_relative_pos(hwnd, button_rx, button_ry)
            pyautogui.click()
        time.sleep(0.5)



### main
print('复读姬 v0.0.01a by rmxlinux (dandinking@buaa.edu.cn)\n温馨提示：复读前请清空剪贴板，避免剪贴板内容泄露。\n')
print('请输入QQ会话名（群名或者用户名，不必全部匹配，输入标志关键词即可）')
key_word = input()
win32gui.EnumWindows(get_window_callback, windows)
key_hwnd = 0
for hwnd, title in windows:
    #print(f'{hwnd} {title}')
    if title.find(key_word) != -1:
        key_hwnd = hwnd
        break
#print(key_hwnd)
print('请点击输入文字区域')
listener = mouse.Listener(on_click=on_click)
listener.start()
event.wait()
text_rx, text_ry = get_relative_pos(key_hwnd)
event = threading.Event()
print('请点击最新消息的左下角，保证鼠标指针在文本之内')
listener = mouse.Listener(on_click=on_click)
listener.start()
event.wait()
chat_rx, chat_ry = get_relative_pos(key_hwnd)
event = threading.Event()
print('请点击发送按钮')
listener = mouse.Listener(on_click=on_click)
listener.start()
event.wait()
button_rx, button_ry = get_relative_pos(key_hwnd)
print('开始复读，按esc键结束')

launch(key_hwnd, text_rx, text_ry, chat_rx, chat_ry, button_rx, button_ry)