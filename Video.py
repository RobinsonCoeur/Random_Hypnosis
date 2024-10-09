import vlc
import time
import keyboard
import mouse

import requests
from bs4 import BeautifulSoup

import pygame
import pyWinhook as pyHook

import WindowsAccess as win
import HypnotubeAccess as acchyp

class Video:
    def __init__(self, link, mode: str, localFile: bool = True, website: str = "hypnotube") -> None:

        self.mediaPlayer = vlc.MediaPlayer()
        pygame.init()

        self.hypnotubeAccess = acchyp.HypnotubeAccess()

        self.hm = pyHook.HookManager()

        self.exitType = 0 #0 running, 1 video over, 2 forced

        self.windowAccess = win.WindowsAccess()

        self.mode = mode

        self.websitesList = ["hypnotube", "xhamster"]

        if localFile:
            self.file = link
        else:
            if website  == "hypnotube":
                self.file = self.hypnotubeAccess.extractVideoFromLink(link)
                print(self.file)

        pass

    def getExitType(self):
        return self.exitType

    def exitVideo(self):
        self.windowAccess.toggleMuteAllApps (False)
        self.mediaPlayer.stop()
        pygame.quit()
        self.hm.UnhookKeyboard()
        self.hm.UnhookMouse()
        self.windowAccess.showTaskBar()
        
    def blockKeys(self):
        def onKeyboardEvent(event):
            if event.Key.lower() in ['tab','alt']:#Keys to block:
                return False    # block these keys
    
            else:
            # return True to pass the event to other handlers
                return True

        def onMouseEvent(event):
            return False

        self.hm.MouseAll = onMouseEvent
        self.hm.HookMouse()

        # watch for all keyboard events
        self.hm.KeyDown = onKeyboardEvent
        # set the hook
        self.hm.HookKeyboard()
        

    def launchVideo(self):
        media = vlc.Media(self.file)
        self.mediaPlayer.set_media(media)

        self.mediaPlayer.set_fullscreen(True)
        self.mediaPlayer.play()
        self.exitType = 0

        start = time.time()
        time.sleep(0.8)

        self.windowAccess.toggleMuteAllApps(True)

        try:
            self.windowAccess.bringWindowToForeground('VLC (Direct3D11 output)')
        except:
            pass

        try:
            self.windowAccess.minimizeWindow("Picture in Picture")
        except:
            pass
        
        self.windowAccess.hideTaskBar()

        self.blockKeys()
        
        while True:
            pygame.event.pump()
            if time.time() - start >= self.mediaPlayer.get_length()/1000 - 0.5:
                self.exitType = 1
                self.exitVideo()
                break
            if keyboard.is_pressed("q") and self.mode == "Soft":
                self.exitType = 2
                self.exitVideo()
                break
            time.sleep(0.1)

#vid = Video("https://xhamster.com/videos/i-will-turn-you-into-a-mindless-cocksucker-hypnosis-master-11530939", False, "xhamster")