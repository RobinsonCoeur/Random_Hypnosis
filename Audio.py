import pygame
from mutagen.mp3 import MP3

import WindowsAccess as win

import time

import keyboard

class Audio():
    
    def __init__(self, linkToAudioFile) -> None:
        self.link = linkToAudioFile
        self.exitType = 0

        pygame.mixer.init()

        self.windowAccess = win.WindowsAccess()

        pass

    def getExitType(self):
        return self.exitType

    def exitAudio(self):
        self.windowAccess.toggleMuteAllApps (False)
        pygame.quit()
        pass

    def launchAudio(self):
        pygame.mixer.music.load(self.link)

        self.windowAccess.toggleMuteAllApps(True)

        pygame.mixer.music.play()
        start = time.time()

        while True:
            if time.time() - start >=  MP3(self.link).info.length:
                self.exitType = 1
                self.exitAudio()
                break
            if keyboard.is_pressed("q"):
                self.exitType = 2
                self.exitAudio()
                break
            time.sleep(0.1)

        pass