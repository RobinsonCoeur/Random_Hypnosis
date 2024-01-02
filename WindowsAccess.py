from pywinauto.findwindows    import find_window
from pywinauto import mouse
import win32gui 
import win32con
from ctypes import windll

class WindowsAccess:
    def __init__(self) -> None:
        pass

    def showTaskBar(self):
        taskBar = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
        windll.user32.ShowWindow(taskBar, 9)

    def hideTaskBar(self):
        taskBar = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
        windll.user32.ShowWindow(taskBar, 0)

    def bringWindowToForeground(self, windowName):
        id = find_window(title=windowName) 
        mouse.move(coords=(-10000, 500))
                
        win32gui.ShowWindow(id,5)
        win32gui.SetForegroundWindow(id)

    def minimizeWindow(self, windowName):
        id = find_window(title=windowName) 
        mouse.move(coords=(-10000, 500))
                
        win32gui.ShowWindow(id, win32con.SW_MINIMIZE)