import threading
import time
from ctypes import POINTER, c_ulong, Structure, c_ushort, c_short, c_long, byref, windll, pointer, sizeof, Union

import PyHook3
import pythoncom
import wx

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


class MainWindow(wx.Frame):
    minTime = 0.05
    press_the_trigger_button = False
    onlyLoL = True
    currentKey = "Capital"
    GongSu = 1.8
    QianYao = 0.45
    dc = 1.0 / GongSu
    qy = dc * QianYao
    hy = dc - qy

    def onKeyDown(self, event):
        if event.Key == self.currentKey:
            self.press_the_trigger_button = True
            if self.onlyLoL and not self.isPause:
                # 按下 C 显示攻击距离,并且仅选中英雄
                sendkey(0x2e, 1)
            return self.isPause
        elif event.Key == "Up":
            self.update_number(self.text_num1, True, 0.6, 3.0, 0.02)
            self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE ^ (
                    wx.MAXIMIZE_BOX | wx.SYSTEM_MENU) | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW)
            self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE ^ (
                    wx.MAXIMIZE_BOX | wx.SYSTEM_MENU) | wx.FRAME_TOOL_WINDOW)
            return False
        elif event.Key == "Down":
            self.update_number(self.text_num1, False, 0.6, 3.0, 0.02)
            return False
        elif event.Key == "Right":
            self.update_number(self.text_num2, True, 0, 1, 0.01)
            return False
        elif event.Key == "Left":
            self.update_number(self.text_num2, False, 0, 1, 0.01)
            return False
        elif event.Key == "Prior":
            self.isPause = False
            self.SetTransparent(255)
            return False
        elif event.Key == "Next":
            self.isPause = True
            self.SetTransparent(90)
            return False
        elif event.Key == "Insert":
            self.start_setting = True
            return False
        elif self.start_setting:
            self.currentKey = event.Key
            self.start_setting = False
            return False
        return True

    def onKeyUp(self, event):
        if event.Key == self.currentKey:
            self.press_the_trigger_button = False
            if self.onlyLoL:
                # 拿开 C 取消攻击距离显示,并且取消仅选中英雄
                sendkey(0x2e, 0)
            return self.isPause
        return True

    def action(self):
        while True:
            if self.press_the_trigger_button and not self.isPause:
                # process_time = time.time()
                self.click(0x2c, self.qy)
                self.click(0x2d, self.hy)
                # ys = time.time() - process_time - self.dc
                # print('单次攻击时间:', round(self.dc, 3), '前摇', round(self.qy, 3), '后摇', round(self.hy, 3), '摇损', ys * 1000)
            else:
                time.sleep(0.01)

    def click(self, key, click_time):
        while click_time > self.minTime and self.press_the_trigger_button:
            process_time = time.time()
            sendkey(key, 1)
            sendkey(key, 0)
            time.sleep(self.minTime)
            click_time = click_time - (time.time() - process_time)
        if self.press_the_trigger_button and click_time > 0:
            sendkey(key, 1)
            sendkey(key, 0)
            time.sleep(click_time)

    def key_listener(self, ):
        hm = PyHook3.HookManager()
        hm.KeyDown = self.onKeyDown
        hm.KeyUp = self.onKeyUp
        hm.HookKeyboard()
        pythoncom.PumpMessages()

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, pos=(500, 500), style=wx.DEFAULT_FRAME_STYLE ^ (
                wx.MAXIMIZE_BOX | wx.SYSTEM_MENU) | wx.FRAME_TOOL_WINDOW,
                          size=(55, 75))
                          # size=(70, 70))

        self.SetBackgroundColour("#ffffff")

        self.isPause = False
        self.start_setting = False

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.text_num1 = wx.StaticText(self, name="aa", label=str(self.GongSu), size=(-1, -1), style=wx.ALIGN_CENTER)

        self.text_num1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))

        self.text_num1.SetForegroundColour('#FF0000')
        self.sizer1.Add(self.text_num1, flag=wx.ALIGN_CENTER)

        self.text_num2 = wx.StaticText(self, name="aa", label=str(self.QianYao), size=(-1, -1), style=wx.ALIGN_CENTER)

        self.text_num2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))

        self.text_num2.SetForegroundColour('#0000FF')

        self.sizer2.Add(self.text_num2, flag=wx.ALIGN_CENTER)

        self.sizer.Add(self.sizer1)
        self.sizer.Add(self.sizer2)
        self.sizer.Add(self.sizer3)

        self.SetSizer(self.sizer)
        self.Show(True)

        self.thread_key = threading.Thread(target=self.action)
        self.thread_action = threading.Thread(target=self.key_listener)
        self.thread_key.daemon = True
        self.thread_action.daemon = True
        self.thread_key.start()
        self.thread_action.start()

    def update_number(self, who, isUp, min, max, min_diff):
        if isUp:
            num = float(who.Label) + min_diff
        else:
            num = float(who.Label) - min_diff
        num = round(num, 2)
        if num < min:
            num = min
        if num > max:
            num = max
        if who == self.text_num1:
            self.GongSu = num
        elif who == self.text_num2:
            self.QianYao = num
        self.dc = 1.0 / self.GongSu
        self.qy = self.dc * self.QianYao
        self.hy = self.dc - self.qy
        num = str(num)
        if len(num) > 3:
            num = num[0:4]
        who.SetLabel(num)


app = wx.App(False)
ui = MainWindow(None, "摇头怪!")
app.MainLoop()
