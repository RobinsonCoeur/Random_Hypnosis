from pywinauto.findwindows    import find_window
from pywinauto import mouse
import win32gui 
import win32con
import win32process
from ctypes import windll

from subprocess import check_output
import psutil

from pycaw.pycaw import AudioUtilities

class WindowsAccess:
    def __init__(self) -> None:

        self.browsersClassNames = {
            "Opera GX": "Chrome_WidgetWin_1",
            "Edge": "Chrome_WidgetWin_1"
        }

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

    def toggleMuteAllApps(self, mute: bool):
        idList = []
        for item in psutil.process_iter():
            if item.name() != 'python3.10.exe' and item.name() != 'Random Hypnosis Program.exe':
                idList.append(item.pid)

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            for id in idList:
                if session.Process and session.Process.pid == id:
                    session.SimpleAudioVolume.SetMute(mute, None)
        
#win = WindowsAccess()
#win.toggleMuteBrowser(False)