import json
import threading
import time
from ctypes import POINTER, c_ulong, Structure, c_ushort, c_short, c_long, byref, windll, pointer, sizeof, Union

import requests
import wx
import urllib3

urllib3.disable_warnings()
zhilianUrl = "https://127.0.0.1:2999/liveclientdata/activeplayer"
# <editor-fold desc="图片识别攻速部分">
def getAttackSpeed(x_begin=385, y_begin=1010, x_end=433, y_end=1036):
    # https://127.0.0.1:2999/liveclientdata/activeplayer
    # activePlayer.championStats.attackSpeed
    try:
        r = requests.get(zhilianUrl, verify=False)
        if r.ok:
            lolJson = r.text
            data = json.loads(lolJson)
            return float(data["championStats"]["attackSpeed"])
        else:
            return None
    except:
        return None


# </editor-fold>


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

import wx.adv


# <editor-fold desc="系统托盘部分">
class TaskBarIcon(wx.adv.TaskBarIcon):
    ID_About = wx.NewId()
    ID_Close = wx.NewId()

    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='icon.ico'), '走A吧少年！')  # wx.ico为ico图标文件
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnClose, id=self.ID_Close)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    def OnAbout(self, event):
        wx.MessageBox("本程序前提是基于LOL改键,不用担心封号\n"
                      "请进游戏到设置修改:\n"
                      "快捷攻击型移动，选择设置成 Z \n"
                      "玩家移动点击，选择设置成 X \n"
                      "仅针对目标英雄设置为 C \n"
                      "最好把窗口设置为无边框模式或者窗口模式\n"
                      "最好再设置下优先攻击鼠标最近的单位，这样就可以鼠标指哪打那\n"
                      "按键说明：\n"
                      "CapsLock - 触发走A\n"
                      "上下左右 - 调整参数\n"
                      "Esc - 最小化到托盘区\n"
                      "鼠标中间滚轮按下 - 设置攻速识别位置"
                      "详细说明：https://github.com/miqt/LOLGameTools\n"
                      "QQ群：209622340\n"
                      "联系作者：miqtdev@163.com", '使用帮助')

    def OnClose(self, event):
        self.Destroy()
        self.frame.Destroy()

    # 右键菜单
    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_About, '使用帮助')
        menu.Append(self.ID_Close, '退出')
        return menu


# </editor-fold>

class MainWindow(wx.Frame):
    minTime = 0.1
    onlyLoL = True
    currentKey = "Capital"
    GongSu = 1.7
    QianYao = 0.35
    YDBC = 0.0
    dc = 1.0 / GongSu
    qy = dc * QianYao
    hy = dc - qy + YDBC

    x_begin = 528 - 142
    y_begin = 1069 - 63
    x_end = 528
    y_end = 1069

    press_the_trigger_button = False

    def onKeyDown(self, event):
        if event.Key == self.currentKey:
            self.press_the_trigger_button = True
            if self.onlyLoL and not self.isPause:
                # 按下 C 显示攻击距离,并且仅选中英雄
                sendkey(0x2e, 1)
            return self.isPause
        elif event.Key == "Right":
            self.update_number(self.text_num2, True, 0, 1, 0.01)
            self.Iconize(False)
            return self.isPause
        elif event.Key == "Left":
            self.update_number(self.text_num2, False, 0, 1, 0.01)
            self.Iconize(False)
            return self.isPause
        elif event.Key == "Prior":
            self.isPause = False
            self.SetTransparent(255)
            self.message_text.Label = "已启动,按住[" + self.currentKey + "]走A"
            self.Iconize(False)
            return False
        elif event.Key == "Next":
            self.isPause = True
            self.SetTransparent(90)
            self.message_text.Label = "已关闭"
            self.Iconize(False)
            return False
        elif event.Key == "Insert":
            self.start_setting = True
            self.currentKey = ""
            self.message_text.Label = "按任意键完成绑定"
            self.Iconize(False)
            return False
        elif not self.IsIconized() and event.Key == "Escape":
            self.Iconize(True)
            return False
        elif self.start_setting:
            self.currentKey = event.Key
            self.start_setting = False
            self.message_text.Label = "已经绑定到：" + self.currentKey
            self.Iconize(False)
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
                process_time = time.time()
                # 天使前置按 E 10 (Q), 11 (W), 12 (E), 13 (R)
                # self.click(0x10, 0)
                self.click(0x2c, self.qy)
                self.click(0x2d, self.hy)
                ys = time.time() - process_time - self.dc - self.YDBC
                # self.message_text.Label = (str(round(self.dc, 3)) + 'A/' + str(round(self.qy, 3)) + 'Z/' +
                #                            str(round(self.hy, 3)) + 'X/' + str(round(ys, 3)))
            else:
                time.sleep(0.01)

    def click(self, key, click_time):
        # 按照一定的频率高速点击
        while click_time > self.minTime and self.press_the_trigger_button:
            process_time = time.time()
            sendkey(key, 1)
            sendkey(key, 0)
            time.sleep(self.minTime)
            click_time = click_time - (time.time() - process_time)
        # 剩余时间不足最小点击频率单位，直接点击一次，然后等待到剩余时间结束
        if self.press_the_trigger_button and click_time >= 0:
            sendkey(key, 1)
            sendkey(key, 0)
            time.sleep(click_time)

    def key_listener(self, ):
        import PyHook3
        import pythoncom
        hm = PyHook3.HookManager()
        hm.KeyDown = self.onKeyDown
        hm.KeyUp = self.onKeyUp
        hm.HookKeyboard()
        hm.HookMouse()
        pythoncom.PumpMessages()

    def listenerAttackSpeed(self, ):
        # 新线程识别攻速，防止因为识别耗时阻塞走A线程
        while True:
            # time.sleep(0.01)
            speed = getAttackSpeed(x_begin=self.x_begin, y_begin=self.y_begin, x_end=self.x_end, y_end=self.y_end)
            if speed is None:
                continue
            if speed <= 0 or speed >= 6.0:
                continue
            if self.GongSu == speed:
                continue
            self.GongSu = speed
            self.dc = 1.0 / self.GongSu
            self.qy = self.dc * self.QianYao
            self.hy = self.dc - self.qy + self.YDBC

    def OnClose(self, event):
        # self.taskBarIcon.Destroy()
        # self.Destroy()
        self.Iconize(True)

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, pos=wx.DefaultPosition, style=wx.DEFAULT_FRAME_STYLE ^ (
                wx.MAXIMIZE_BOX | wx.SYSTEM_MENU) | wx.STAY_ON_TOP,
                          size=(176, 182))

        self.SetBackgroundColour("#ffffff")
        self.SetIcon(wx.Icon('icon.ico'))
        self.taskBarIcon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.isPause = False
        self.start_setting = False

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer5 = wx.BoxSizer(wx.HORIZONTAL)


        self.text2 = wx.StaticText(self, name="aa", label="前摇", size=(40, -1), style=wx.ALIGN_CENTER)
        self.text_num2 = wx.StaticText(self, name="aa", label=str(self.QianYao), size=(60, -1), style=wx.ALIGN_CENTER)
        self.text2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.text_num2.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        self.text2.SetForegroundColour('#000000')
        self.text_num2.SetForegroundColour('#0000FF')
        self.button_up2 = wx.Button(self, name="up2", label="→", size=(30, 30))
        self.button_down2 = wx.Button(self, name="down2", label="←", size=(30, 30))
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_up2)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_down2)
        self.sizer2.Add(self.text2, flag=wx.ALIGN_CENTER)
        self.sizer2.Add(self.text_num2, flag=wx.ALIGN_CENTER)
        self.sizer2.Add(self.button_down2, flag=wx.ALIGN_CENTER)
        self.sizer2.Add(self.button_up2, flag=wx.ALIGN_CENTER)

        self.text3 = wx.StaticText(self, name="aa", label="移补", size=(40, -1), style=wx.ALIGN_CENTER)
        self.text_num3 = wx.StaticText(self, name="aa", label=str(self.YDBC), size=(60, -1), style=wx.ALIGN_CENTER)
        self.text3.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.text_num3.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        self.text3.SetForegroundColour('#000000')
        self.text_num3.SetForegroundColour('#000000')
        self.button_up3 = wx.Button(self, name="up3", label="+", size=(30, 30))
        self.button_down3 = wx.Button(self, name="down3", label="-", size=(30, 30))
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_up3)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_down3)
        self.sizer3.Add(self.text3, flag=wx.ALIGN_CENTER)
        self.sizer3.Add(self.text_num3, flag=wx.ALIGN_CENTER)
        self.sizer3.Add(self.button_down3, flag=wx.ALIGN_CENTER)
        self.sizer3.Add(self.button_up3, flag=wx.ALIGN_CENTER)

        self.button_start = wx.Button(self, name="start", label="开", size=(40, 30))
        self.button_stop = wx.Button(self, name="stop", label="关", size=(40, 30))
        self.button_setting = wx.Button(self, name="setting", label="设触发键", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_start)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_stop)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_setting)
        self.sizer4.Add(self.button_start, flag=wx.ALIGN_CENTER)
        self.sizer4.Add(self.button_stop, flag=wx.ALIGN_CENTER)
        self.sizer4.Add(self.button_setting, flag=wx.ALIGN_CENTER)

        self.message_text = wx.StaticText(self, name="aa", label="已启动,按住[" + self.currentKey + "]走A\n进入游戏后自动获取攻速")
        self.message_text.SetForegroundColour('#000000')
        self.sizer5.Add(self.message_text)

        # self.sizer.Add(self.sizer1)
        self.sizer.Add(self.sizer2)
        self.sizer.Add(self.sizer3)
        self.sizer.Add(self.sizer4)
        self.sizer.Add(self.sizer5)

        self.SetSizer(self.sizer)
        self.Show(True)

        self.thread_key = threading.Thread(target=self.action)
        self.thread_action = threading.Thread(target=self.key_listener)
        self.thread_listenerAttackSpeed = threading.Thread(target=self.listenerAttackSpeed)
        self.thread_listenerAttackSpeed.daemon = True
        self.thread_key.daemon = True
        self.thread_action.daemon = True
        self.thread_listenerAttackSpeed.start()
        self.thread_key.start()
        self.thread_action.start()

    def onClick(self, event):
        name = event.GetEventObject().GetName()
        if name == "up1":
            self.update_number(self.text_num1, True, 0.1, 3.5, 0.1)
        elif name == "down1":
            self.update_number(self.text_num1, False, 0.1, 3.5, 0.1)
        elif name == "up2":
            self.update_number(self.text_num2, True, 0.1, 0.9, 0.05)
        elif name == "down2":
            self.update_number(self.text_num2, False, 0.1, 0.9, 0.05)
        elif name == "up3":
            self.update_number(self.text_num3, True, 0.0, 1.0, 0.01)
        elif name == "down3":
            self.update_number(self.text_num3, False, 0.0, 1.0, 0.01)
        elif name == "start":
            self.isPause = False
            self.SetTransparent(255)  # 设置透明
            self.message_text.Label = "已启动,按住[" + self.currentKey + "]走A"
            pass
        elif name == "stop":
            self.isPause = True
            self.SetTransparent(90)  # 设置透明
            self.message_text.Label = "已关闭"
        elif name == "setting":
            self.start_setting = True
            self.currentKey = ""
            self.message_text.Label = "按任意键完成绑定"
            pass

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
        if who == self.text_num2:
            self.QianYao = num
        elif who == self.text_num3:
            self.YDBC = num
        self.dc = 1.0 / self.GongSu
        self.qy = self.dc * self.QianYao
        self.hy = self.dc - self.qy + self.YDBC
        num = str(num)
        if len(num) > 3:
            num = num[0:4]
        who.SetLabel(num)


app = wx.App(False)
ui = MainWindow(None, "刀!")
ui.Centre()
app.MainLoop()
