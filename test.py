import win32api
import win32con
import win32gui
import win32print


def getMousePos():
    hDC = win32gui.GetDC(0)
    pos = win32api.GetCursorPos()
    print(pos)
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    print(width, height)
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    print(w, h)
    zoomx = w / width
    zoomh = h / height
    pos = (pos[0] * zoomx, pos[1] * zoomh)
    return pos


getMousePos()
