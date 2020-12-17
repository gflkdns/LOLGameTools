import threading
import time
from ctypes import *  # 获取屏幕上某个坐标的颜

import PyHook3
import pythoncom

# <editor-fold desc="模拟点击部分">
PUL = POINTER(c_ulong)


class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]


class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]


def get_mpos():
    orig = POINT()
    windll.user32.GetCursorPos(byref(orig))
    return int(orig.x), int(orig.y)


def set_mpos(pos):
    x, y = pos
    windll.user32.SetCursorPos(x, y)


def move_click(pos, move_back=False):
    origx, origy = get_mpos()
    set_mpos(pos)
    FInputs = Input * 2
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
    ii2_ = Input_I()
    ii2_.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))
    x = FInputs((0, ii_), (0, ii2_))
    windll.user32.SendInput(2, pointer(x), sizeof(x[0]))
    if move_back:
        set_mpos((origx, origy))
        return origx, origy


def sendkey(scancode, pressed):
    FInputs = Input * 1
    extra = c_ulong(0)
    ii_ = Input_I()
    flag = 0x8
    ii_.ki = KeyBdInput(0, 0, flag, 0, pointer(extra))
    InputBox = FInputs((1, ii_))
    if scancode is None:
        return
    InputBox[0].ii.ki.wScan = scancode
    InputBox[0].ii.ki.dwFlags = 0x8

    if not (pressed):
        InputBox[0].ii.ki.dwFlags |= 0x2

    windll.user32.SendInput(1, pointer(InputBox), sizeof(InputBox[0]))


# </editor-fold>


def getRgb(x, y):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)  # 获取颜值
    pixel = gdi32.GetPixel(hdc, x, y)  # 提取RGB值
    r = pixel & 0x0000ff
    g = (pixel & 0x00ff00) >> 8
    b = pixel >> 16
    return [r, g, b]


def get_color(r, g, b):
    if (r < 127 and g < 127 and b > 127):
        return ("蓝")
    elif (r < 127 and g > 127 and b < 127):
        return ("绿")
    elif (r > 127 and g < 127 and b < 127):
        return ('红')
    elif (r > 127 and g > 127 and b < 127):
        return ("黄")
    elif (r > 127 and g < 127 and b > 127):
        return ("紫")
    elif (r < 127 and g > 127 and b > 127):
        return ("青")
    elif (r > 127 and g > 127 and b > 127):
        return ('白')
    elif (r < 127 and g < 127 and b < 127):
        return ('黑')

def down(event):
    # 10 (Q), 11 (W), 12 (E), 13 (R)
    key = event.Key
    global req_color
    if key == "E":
        req_color = '黄'
        threading.Thread(target=click).start()
    elif key == "W":
        global self_w
        if not self_w:
            req_color = '蓝'
            threading.Thread(target=click).start()
        else:
            self_w = False
    elif key == "T":
        req_color = '红'
        threading.Thread(target=click).start()
    elif key == "R":
        req_color = '黄'
        threading.Thread(target=click).start()
    return True





self_w = False
req_color = "黄"


def click():
    # 先按一下W
    global self_w
    self_w = True
    sendkey(0x11, 1)
    sendkey(0x11, 0)
    global req_color
    print('开始监听', req_color)
    process_time = time.time()
    while time.time() - process_time < 5:
        r, g, b = getRgb(x, y)
        color = get_color(r, g, b)
        if color == req_color:
            self_w = True
            sendkey(0x11, 1)
            sendkey(0x11, 0)
            print('抽牌成功', req_color)
            return
        time.sleep(0.05)
    print('抽牌失败', req_color)


def move(event):
    global x, y
    x = event.Position[0]
    y = event.Position[1]
    print("当前取色坐标：", x, y, '祝您游戏愉快')
    return True


def action():
    hm = PyHook3.HookManager()
    hm.KeyDown = down
    hm.MouseMiddleDown = move
    hm.HookKeyboard()
    hm.HookMouse()
    pythoncom.PumpMessages()


x = 100
y = 100
print('一切尽在卡牌中！，光速抽牌，已经启动：E：黄牌，W：蓝牌，T：红牌，大招自动黄牌')
print('请按下 鼠标中间滑轮按键 确定卡牌取色位置：')
action()

