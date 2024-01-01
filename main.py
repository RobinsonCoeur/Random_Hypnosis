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
        windll.user32.ShowWindow(windowName, 0)

    def minimizeWindow(self, windowName):
        id = find_window(title=windowName) 
        mouse.move(coords=(-10000, 500))
                
        win32gui.ShowWindow(id, win32con.SW_MINIMIZE)


class Video:
    def __init__(self, filePath) -> None:

        self.mediaPlayer = vlc.MediaPlayer()
        pygame.init()

        self.exitType = 0 #0 running, 1 video over, 2 forced

        self.windowAccess = WindowsAccess()
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

        self.eventSchedule = sched.scheduler(time.time, time.sleep)
        self.video = ""
        self.currentIdInQueue = 0
        self.run = False

        self.safetyTime = 30 #used to start another video min. 30 sec after forced exit
        self.launchTimeRange =  3600 #in seconds

        pass

    def getSafetyTime(self):
        return self.safetyTime
    
    def setSafetyTime(self, newTime):
        self.safetyTime = newTime

    def getLaunchTimeRange(self):
        return self.launchTimeRange
    
    def setLaunchTimeRange(self, newTime):
        self.launchTimeRange = newTime

    def cancelQueue(self):
        self.eventSchedule.cancel(self.currentIdInQueue)

    def setRunFlag(self, state):
        self.run = state

    def randomVideosEvent(self, folderPath: str):
        def loadVideo():
            files = os.listdir(folderPath)
            chosenFile = files[random.randint(0, len(files)-1)]

            video = Video(r"{}".format(folderPath + "\\" + chosenFile))
            video.launchVideo()
            exitType = video.getExitType()

            if self.run:
                if exitType == 1:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadVideo)
                if exitType == 2:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(self.safetyTime, self.launchTimeRange+self.safetyTime), 1, loadVideo)
        
        self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadVideo)
        self.eventSchedule.run()

class UserData:
    def __init__(self, path: str = "", time: float = 2.50) -> None:

        self.curDir = os.getcwd()

        self.pathToFolder = path
        self.timeRange = time
        self.userDataStorage = [self.pathToFolder, self.timeRange]

        pass 

    def initSaveFile(self):
        if not os.path.isfile(self.curDir + "\\save.csv"):
            open(self.curDir + "\\save.csv", "w", newline='')

    def getPathToFolder(self):
        return self.pathToFolder
    
    def setPathToFolder(self, path: str):
        self.getPathToFolder = path

    def getTimeRange(self):
        return self.pathToFolder
    
    def setTimeRange(self, time: float):
        self.timeRange = time

    def loadUserData(self):
        with open(self.curDir+ "\\save.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.userDataStorage = row

            try:
                self.setPathToFolder(self.userDataStorage[0])
                self.setTimeRange(float(self.userDataStorage[1]))
            except:
                pass

    def saveUserData(self):
        with open("save.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.userData)

class GUI:
    
    def __init__(self) -> None:
        self.userData = UserData()
        self.userData.initSaveFile()
        self.userData.loadUserData()

        self.bufferPath = ""
        self.bufferTimerValue = 0

        self.scheduler = Schedule()

        self.runningSchedule = False

        self.pathValid = False

        self.root = CTk()
        self.windowTitle = "Hypnosis Computer Virus"
        self.root.title(self.windowTitle)
        self.root.geometry('380x420')

        self.setupMenuFrame()

        self.root.after(50, self.checkFrameConditions) 
        self.root.protocol("WM_DELETE_WINDOW", exit)

        self.root.mainloop()

        pass
    
    def loadVlcDownloadPage(self):
        webbrowser.open('https://get.videolan.org/vlc/3.0.11/win64/vlc-3.0.11-win64.exe') 

    def createEntryInFrame(self, frame: CTkFrame, text: str = "", width: int = 100):
        entry = CTkEntry(frame, width = width)
        entry.insert(1, text) 
        
        return entry 

    def verifyPathValidity(self, path: str):
        if os.path.exists(path):
            self.checkBoxPath.select()
            self.checkBoxPath.configure(text="Path is valid")
            self.pathValid = True

            if self.bufferPath != path:
                self.bufferPath = path
                self.userData.setPathToFolder(path)
        else:
            self.checkBoxPath.deselect()
            self.checkBoxPath.configure(text="Path not valid")
            self.pathValid = False

    def updateSliderLabel(self, sliderValue):
        valuesList = str(sliderValue).split(".")
        hrs = valuesList[0]
        inMin = int(valuesList[1])

        if inMin == 5:
            inMin = 50

        self.scaleValue.configure(text = hrs + " hr and " + str(inMin*60/100).split(".")[0] + " min")

        return

    def checkFrameConditions(self):
        pathToFiles = self.linkEntry.get()
        self.verifyPathValidity(pathToFiles)

        sliderValue = self.scale1.get()

        if sliderValue != self.bufferTimerValue:
            self.bufferTimerValue = sliderValue
            self.userData.setTimeRange(sliderValue)

        self.updateSliderLabel(sliderValue)
        self.launchTimeRange = int(sliderValue*60*60) + 1

        self.root.after(50, self.checkFrameConditions)

        return

    def setupMenuFrame(self) -> None:
        menuFrame = CTkFrame(self.root)
        set_appearance_mode("dark")
        menuFrame.pack(side="top", expand=True, fill="both")

        #top frame
        topFrame = CTkFrame(menuFrame, height = 40, width = 400, fg_color = "#2b2b2b", corner_radius=5)
        topFrame.pack(side = TOP)

        self.linkEntry = self.createEntryInFrame(topFrame, '"Path to your video files"', 210)
        self.linkEntry.place(relx = 0.4, rely = 0.5, anchor = CENTER)

        self.checkBoxPath = CTkCheckBox(topFrame, text="Path not valid", onvalue="on", offvalue="off", state = DISABLED, checkbox_width = 15, checkbox_height = 15)
        self.checkBoxPath.place(relx = 0.85, rely = 0.5, anchor = CENTER)

        #middle   
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

        #program status
        rightFrame = CTkFrame(menuFrame, height = 40, width = 100, fg_color = "#2b2b2b", corner_radius=5)
        rightFrame.pack(side = RIGHT)

        self.checkBoxStatus = CTkCheckBox(rightFrame, text="Progam Off", onvalue="on", offvalue="off", state = DISABLED, checkbox_width = 21, checkbox_height = 21)
        self.checkBoxStatus.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        return

    def closeProgram(self):
        self.runningSchedule = False
        self.scheduler.setRunFlag(False)

        self.checkBoxStatus.deselect()
        self.checkBoxStatus.configure(text="Progam Off")
        try:
            self.scheduler.cancelQueue()
        except:
            pass

        return

    def exit(self):
        self.userData.saveUserData()
        self.closeProgram()
        sys.exit()

    def launch(self):

        def videoThread():
            self.scheduler.setLaunchTimeRange(self.launchTimeRange)
            self.scheduler.randomVideosEvent(self.pathToFiles)

        if not self.runningSchedule and self.pathValid:
            winAccess = WindowsAccess()
            winAccess.minimizeWindow(self.windowTitle)

            self.checkBoxStatus.select()
            self.checkBoxStatus.configure(text="Progam On")

            t1=Thread(target=videoThread)
            t1.start()

            self.scheduler.setRunFlag(True)
            self.runningSchedule = True
    

    def clearFrame(self, frame: CTkFrame):
        for widget in frame.winfo_children():
            widget.destroy()
            
        frame.pack_forget()

gui = GUI() 