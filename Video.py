import vlc
import time
import keyboard
import mouse

import requests
from bs4 import BeautifulSoup

import pygame
import pyWinhook as pyHook

import WindowsAccess as win

class Video:
    def __init__(self, linkToVideo, mode: str, localFile: bool = True, website: str = "") -> None:

        self.mediaPlayer = vlc.MediaPlayer()
        pygame.init()

        self.hm = pyHook.HookManager()

        self.exitType = 0 #0 running, 1 video over, 2 forced

        self.windowAccess = win.WindowsAccess()

        self.mode = mode

        self.websitesList = ["hypnotube", "xhamster"]

        if localFile:
            self.file = linkToVideo
        else:
            self.file = self.extractVideoFromLink(linkToVideo, website)

        pass

    def getExitType(self):
        return self.exitType

    def exitVideo(self):
        self.windowAccess.toggleMuteAllApps (False)
        self.mediaPlayer.stop()
        pygame.quit()
        self.hm.UnhookKeyboard()
        self.windowAccess.showTaskBar()
        
    def blockKeys(self):
        def OnKeyboardEvent(event):
            if event.Key.lower() in ['tab','alt']:#Keys to block:
                return False    # block these keys
    
            else:
            # return True to pass the event to other handlers
                return True

        # watch for all keyboard events
        self.hm.KeyDown = OnKeyboardEvent
        # set the hook
        self.hm.HookKeyboard()

    def extractVideoFromLink(self, link: str, website: str):
        file = ""
        #extract file like https://cdn.hypnotube.com/videos/5/f/d/5/d/5fd5d34293d6a.mp4 from link html
        
        if website in self.websitesList:
            page = requests.get(link)
            htmlData = BeautifulSoup(page.content, "html.parser")

            if website == "hypnotube":
                videoSpace = htmlData.find_all("div", class_ = "inner-stage")
                for item in videoSpace:
                    file = item.find_all("source")[0]["src"]

            '''elif website == "xhamster":
                videoSpace = htmlData.find_all("div", id = "player-container")
                for item in videoSpace:
                    file = item.find_all("video")
                    print(file)'''
                    

        return file
        

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
            #mouse.move(10000,0, absolute=True, duration=0)
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