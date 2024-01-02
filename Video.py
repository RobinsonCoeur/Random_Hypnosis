import vlc
import time
import keyboard

import pygame
import pyWinhook as pyHook

import WindowsAccess as win

class Video:
    def __init__(self, filePath) -> None:

        self.mediaPlayer = vlc.MediaPlayer()
        pygame.init()

        self.exitType = 0 #0 running, 1 video over, 2 forced

        self.windowAccess = win.WindowsAccess()
        self.file = filePath

        pass

    def getExitType(self):
        return self.exitType

    def exitVideo(self):
        self.mediaPlayer.stop()
        self.windowAccess.showTaskBar()
        
    def blockKeys(self):
        def OnKeyboardEvent(event):
            if event.Key.lower() in ['tab','alt']:#Keys to block:
                return False    # block these keys
    
            else:
            # return True to pass the event to other handlers
                return True

        hm = pyHook.HookManager()
        # watch for all keyboard events
        hm.KeyDown = OnKeyboardEvent
        # set the hook
        hm.HookKeyboard()

    def launchVideo(self):
        media = vlc.Media(self.file)
        self.mediaPlayer.set_media(media)

        self.mediaPlayer.set_fullscreen(True)
        self.mediaPlayer.play()
        self.exitType = 0

        start = time.time()
        time.sleep(1)

        self.windowAccess.bringWindowToForeground('VLC (Direct3D11 output)')
        self.windowAccess.hideTaskBar()

        self.blockKeys()
        
        while True:
            pygame.event.pump()
            if time.time() - start >= self.mediaPlayer.get_length()/1000 - 0.5:
                self.exitType = 1
                self.exitVideo()
                break
            if keyboard.is_pressed("q"):
                self.exitType = 2
                self.exitVideo()
                break