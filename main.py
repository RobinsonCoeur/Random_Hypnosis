import os 
import sys
import csv

from pywinauto.findwindows    import find_window
from pywinauto import mouse
import win32gui 
import win32con
from ctypes import windll

import keyboard
import pyWinhook as pyHook
import random

import vlc
import pygame

import webbrowser

import sched
import time

from customtkinter import *
from tkinter import *

from threading import *

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
        windll.user32.ShowWindow(self.taskBar, 0)

class Video:
    def __init__(self, filePath) -> None:

        self.mediaPlayer = vlc.MediaPlayer()
        pygame.init()

        self.windowAccess = WindowsAccess()
        self.file = filePath

        pass

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
        time.sleep(0.8)

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

class Schedule:
    def __init__(self) -> None:

        self.video = 0

        pass

    def randomVideosEvent(self, folderPath: str, safetyTime: int, launchTimeRange: int):
        def loadVideo():
            files = os.listdir(folderPath)
            chosenFile = files[random.randint(0, len(files)-1)]

            video = Video(r"{}".format(folderPath + "\\" + chosenFile))
            video.launchVideo()

            if self.run:
                if self.exitType == 1:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, launchTimeRange), 1, loadVideo)
                if self.exitType == 2:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(safetyTime, launchTimeRange+safetyTime), 1, loadVideo)
        
        self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadVideo)
        self.eventSchedule.run()

class GUI:
    
    def __init__(self) -> None:
        self.root = CTk()
        self.windowTitle = "Hypnosis Computer Virus"
        self.root.title(self.windowTitle)
        self.root.geometry('380x420')

        self.taskBar = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
        windll.user32.ShowWindow(self.taskBar, 9)

        self.mediaPlayer = vlc.MediaPlayer()
        pygame.init()

        self.eventSchedule = sched.scheduler(time.time, time.sleep)
        self.exitType = 0 #0 running, 1 video over, 2 forced
        self.run = True
        self.runningVideo = False
        self.currentIdInQueue = 0
        
        self.safetyTime = 30 #used to start another video min. 30 sec after forced exit
        self.launchTimeRange =  3600 #in seconds

        self.userData = [] #pathToFile
        
        self.setupMenuFrame()

        self.root.after(50, self.checkFrameConditions) 
        self.root.protocol("WM_DELETE_WINDOW", exit)
        self.root.mainloop()
    
    def loadVlcDownloadPage(self):
        webbrowser.open('https://get.videolan.org/vlc/3.0.11/win64/vlc-3.0.11-win64.exe') 

    def createEntryInFrame(self, frame: CTkFrame, text: str = "", width: int = 100):
        entry = CTkEntry(frame, width = width)
        entry.insert(1, text) 
        entry.pack()
        
        return entry
    
    def savePathToFiles(self):
        self.pathToFiles = self.linkEntry.get()

        with open("save.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow("")

        return

    def checkFrameConditions(self):
        val = str(self.scale1.get()).split(".")
        hrs = val[0]
        inMin = int(val[1])

        if inMin == 5:
            inMin = 50

        self.scaleValue.configure(text = hrs + " hr and " + str(inMin*60/100).split(".")[0] + " min")
        self.root.after(50, self.checkFrameConditions)

        self.launchTimeRange = int(self.scale1.get()*60*60) + 1

        return

    def setupMenuFrame(self) -> None:
        menuFrame = CTkFrame(self.root)
        set_appearance_mode("dark")
        menuFrame.pack(side="top", expand=True, fill="both")

        self.linkEntry = self.createEntryInFrame(menuFrame, '"Path to your video files"', 210)
        
        menuFrame.buttonLaunch = CTkButton(master = menuFrame, text="Launch !", 
                                  command= lambda : self.launch())
        menuFrame.buttonLaunch.place(relx = 0.5, rely = 0.3, anchor = CENTER)

        menuFrame.buttonVLC = CTkButton(master = menuFrame, text="Download VLC ?", 
                                  command= lambda : self.loadVlcDownloadPage())
        menuFrame.buttonVLC.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        menuFrame.buttonQuit = CTkButton(master = menuFrame, text="Exit App", 
                                  command= lambda : self.exit())
        menuFrame.buttonQuit.place(relx = 0.5, rely = 0.6, anchor = CENTER)

        menuFrame.buttonCloseVirus = CTkButton(master = menuFrame, text="Turn off the program", 
                                  command= lambda : self.closeProgram())
        menuFrame.buttonCloseVirus.place(relx = 0.5, rely = 0.4, anchor = CENTER)

        label = CTkLabel(menuFrame, width = 100, text = "Input max time between videos", fg_color = ("white", "#1c6ba3"), corner_radius=8)
        label.pack(side = BOTTOM)

        #time input
        bottomFrame = CTkFrame(menuFrame, height = 40, width = 350, fg_color = "#2b2b2b", corner_radius=5)
        bottomFrame.pack(side = BOTTOM)

        self.scale1 = CTkSlider(bottomFrame, from_= 0, to=5, orientation="horizontal", number_of_steps = 20)
        self.scale1.place(relx = 0.3, rely = 0.5, anchor = CENTER)

        self.scaleValue = CTkLabel(bottomFrame, width = 10, text = "0", fg_color = ("white", "#1c6ba3"), corner_radius= 5)
        self.scaleValue.place(relx = 0.80, rely = 0.5, anchor = CENTER)

        return

    def closeProgram(self):
        self.run = False
        try:
            self.eventSchedule.cancel(self.currentIdInQueue)
        except:
            pass

        return

    def exit(self):
        self.closeProgram()
        sys.exit()

    def launch(self):

        def videoThread():
            self.randomEvent(self.userData[0])

        if not self.runningVideo:
            id = find_window(title=self.windowTitle) 
            mouse.move(coords=(-10000, 500))
                
            win32gui.ShowWindow(id, win32con.SW_MINIMIZE)

            t1=Thread(target=videoThread)
            t1.start()

            self.runningVideo = True

    def exitVideo(self):
        self.mediaPlayer.stop()
        windll.user32.ShowWindow(self.taskBar, 9)
        self.runningVideo = False
        
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

    def video(self, file):
        media = vlc.Media(file)
        self.mediaPlayer.set_media(media)

        self.mediaPlayer.set_fullscreen(True)
        self.mediaPlayer.play()
        self.exitType = 0

        start = time.time()
        time.sleep(0.8)

        id = find_window(title='VLC (Direct3D11 output)') 
        mouse.move(coords=(-10000, 500))
                
        win32gui.ShowWindow(id,5)
        win32gui.SetForegroundWindow(id)
        windll.user32.ShowWindow(self.taskBar, 0)

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

    def randomEvent(self, folderPath):
        def arrangeBoundaries(val1, val2):
            if val1 > val2:
                b = val1
                a = val2
            else:
                a = val1
                b = val2
            return a, b

        def loadVideo():
            files = os.listdir(folderPath)
            chosenFile = files[random.randint(0, len(files)-1)]

            self.video(r"{}".format(folderPath + "\\" + chosenFile))

            if self.run:
                if self.exitType == 1:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadVideo)
                if self.exitType == 2:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(self.safetyTime, self.launchTimeRange+self.safetyTime), 1, loadVideo)
        
        a, b = arrangeBoundaries(5, self.launchTimeRange)
        self.currentIdInQueue = self.eventSchedule.enter(random.randint(a, b), 1, loadVideo)
        self.eventSchedule.run()    
    

    def clearFrame(self, frame: CTkFrame):
        for widget in frame.winfo_children():
            widget.destroy()
            
        frame.pack_forget()

    ##TESTS##
    def testVideoLoading(self):
        self.video(r"F:\Users\cyriletjulia\Documents\Loïc\Musique création\videos\boobs.mp4")

gui = GUI() 