import os 
import sys

import webbrowser

import UserData as user
import Schedule as sch
import WindowsAccess as win

from customtkinter import *
from tkinter import *

from threading import *
#qqqqqqqqqqqqq
class GUI:
    
    def __init__(self) -> None:
        self.userData = user.UserData()
        self.userData.initSaveFile()
        self.userData.loadUserData()

        self.bufferPath = ""
        self.bufferTimerValue = 0

        self.scheduler = sch.Schedule()
        self.video = None

        self.pathValid = False

        self.root = CTk()
        self.windowTitle = "Hypnosis Computer Virus"
        self.root.after(201, lambda :self.root.iconbitmap(self.userData.getCurrentDir() + '\\myIcon.ico'))
        self.root.title(self.windowTitle)
        self.root.geometry('380x420')
        self.frameIndex = 0 #0 menu, 1 settings

        self.labelBgColor = "#3e3261"
        self.labelRad = 25

        self.setupMenuFrame()

        self.root.after(50, self.checkFrameConditions) 
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.root.mainloop()

        pass
    
    def loadVlcDownloadPage(self):
        webbrowser.open('https://get.videolan.org/vlc/3.0.11/win64/vlc-3.0.11-win64.exe') 

    def loadDonationPage(self):
        webbrowser.open("https://www.buymeacoffee.com/murkyshower")

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
        valuesList = str(round(float(sliderValue), 2)).split(".")
        hrs = valuesList[0]
        inMin = int(valuesList[1])
        minList = str(inMin).split()
        print(minList)
        if (len(minList) == 1):
            inMin = int(str(inMin) + "0")
        

        self.scaleValue.configure(text = hrs + " hr and " + str(inMin*60/100).split(".")[0] + " min")

        return

    def checkFrameConditions(self):
        if (self.frameIndex == 0):
            pathToFiles = self.linkEntry.get()
            self.verifyPathValidity(pathToFiles)

            sliderValue = self.scale1.get()

            if sliderValue != self.bufferTimerValue:
                self.bufferTimerValue = sliderValue
                self.userData.setTimeRange(sliderValue)

            self.updateSliderLabel(sliderValue)
            self.launchTimeRange = int(sliderValue*60*60) + 1

        if (self.frameIndex == 1):
            if self.maxTimeEntry.get() != '':
                self.userData.setMaxTime(int(self.maxTimeEntry.get()))

        self.root.after(50, self.checkFrameConditions)

        return

    def setupOptionsGrid(self, masterFrame):
        optionsFrame = CTkFrame(masterFrame, height = 40, width = 400, fg_color = "#2b2b2b", corner_radius=5)
        optionsFrame.pack(side = TOP)

        optionsFrame.buttonLaunch = CTkButton(master = optionsFrame, text="Settings", 
                                  command= lambda : self.setupSettingsFrame(optionsFrame.master), width = 100, height = 19)
        optionsFrame.buttonLaunch.place(relx = 0.15, rely = 0.5, anchor = CENTER)

    def setupMenuFrame(self) -> None:
        menuFrame = CTkFrame(self.root)
        set_appearance_mode("dark")
        menuFrame.pack(side="top", expand=True, fill="both")

        self.setupOptionsGrid(menuFrame)

        #top frame
        topFrame = CTkFrame(menuFrame, height = 40, width = 400, fg_color = "#2b2b2b", corner_radius=5)
        topFrame.pack(side = TOP)

        self.linkEntry = self.createEntryInFrame(topFrame, str(self.userData.getPathToFolder()), 210)
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

        menuFrame.buttonDonations = CTkButton(master = menuFrame, text="Buy me a coffee :)", 
                                  command= lambda : self.loadDonationPage())
        menuFrame.buttonDonations.place(relx = 0.5, rely = 0.6, anchor = CENTER)

        menuFrame.buttonCloseVirus = CTkButton(master = menuFrame, text="Turn off the program", 
                                  command= lambda : self.closeProgram())
        menuFrame.buttonCloseVirus.place(relx = 0.5, rely = 0.4, anchor = CENTER)

        label = CTkLabel(menuFrame, width = 100, text = "Input max time between videos", fg_color = ("white", self.labelBgColor), corner_radius=self.labelRad)
        label.pack(side = BOTTOM)

        #time input
        bottomFrame = CTkFrame(menuFrame, height = 40, width = 350, fg_color = "#2b2b2b", corner_radius=5)
        bottomFrame.pack(side = BOTTOM)

        maxTime = self.userData.getMaxTime()
        self.scale1 = CTkSlider(bottomFrame, from_= 0, to=maxTime, orientation="horizontal", number_of_steps = 20)
        self.scale1.set(self.userData.getTimeRange())
        self.scale1.place(relx = 0.3, rely = 0.5, anchor = CENTER)

        self.scaleValue = CTkLabel(bottomFrame, width = 10, text = "0", fg_color = ("white", self.labelBgColor), corner_radius= self.labelRad)
        self.scaleValue.place(relx = 0.80, rely = 0.5, anchor = CENTER)

        #program status
        rightFrame = CTkFrame(menuFrame, height = 40, width = 100, fg_color = "#2b2b2b", corner_radius=5)
        rightFrame.pack(side = RIGHT)

        self.checkBoxStatus = CTkCheckBox(rightFrame, text="Progam Off", onvalue="on", offvalue="off", state = DISABLED, checkbox_width = 21, checkbox_height = 21)
        self.checkBoxStatus.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        return

    def setupSettingsFrame(self, previousFrame):
        self.frameIndex = 1
        self.clearFrame(previousFrame)

        settingsFrame = CTkFrame(self.root)
        set_appearance_mode("dark")
        settingsFrame.pack(side="top", expand=True, fill="both")  

        #max time
        maxLabel = CTkLabel(settingsFrame, width = 100, text = "Max time (hrs) slider value", fg_color = ("white", self.labelBgColor), corner_radius=self.labelRad)
        maxLabel.place(relx = 0.5, rely = 0.35, anchor = CENTER)

        self.maxTimeEntry = self.createEntryInFrame(settingsFrame, str(self.userData.getMaxTime()), 50)
        self.maxTimeEntry.place(relx = 0.5, rely = 0.45, anchor = CENTER)

        #media type
        mediaChoiceFrame = CTkFrame(settingsFrame, height = 100, width = 300, fg_color = "#2b2b2b", corner_radius=5)
        mediaChoiceFrame.pack(side = TOP)

        def checkboxVideoEvent():
            if checkboxVideo.get() == "on":
                if checkboxAudio.get() == "on":
                    self.userData.setMediaType("both")
                else:
                    self.userData.setMediaType("video")
            else:
                if checkboxAudio.get() == "on":
                    self.userData.setMediaType("audio")
                else:
                    self.userData.setMediaType("none")

            pass

        def checkboxAudioEvent():
            if checkboxAudio.get() == "on":
                if checkboxVideo.get() == "on":
                    self.userData.setMediaType("both")
                else:
                    self.userData.setMediaType("audio")
            else:
                if checkboxVideo.get() == "on":
                    self.userData.setMediaType("video")
                else:
                    self.userData.setMediaType("none")

            pass

        media = self.userData.getMediaType()

        mediaLabel = CTkLabel(mediaChoiceFrame, width = 100, text = "Select what you want to play", fg_color = ("white", self.labelBgColor), corner_radius=self.labelRad)
        mediaLabel.place(relx = 0.5, rely = 0.2, anchor = CENTER)

        check_var = StringVar(value="on")
        checkboxVideo = CTkCheckBox(mediaChoiceFrame, text="Video", command=checkboxVideoEvent,
                                     variable=check_var, onvalue="on", offvalue="off", checkbox_width = 21, checkbox_height = 21)
        checkboxVideo.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        if media == "audio" or media == "none":
            checkboxVideo.deselect()
        
        check_var = StringVar(value="on")
        checkboxAudio = CTkCheckBox(mediaChoiceFrame, text="Audio", command=checkboxAudioEvent,
                                     variable=check_var, onvalue="on", offvalue="off", checkbox_width = 21, checkbox_height = 21)
        checkboxAudio.place(relx = 0.5, rely = 0.8, anchor = CENTER)

        if media == "video" or media == "none":
            checkboxAudio.deselect()

        settingsFrame.leaveButton = CTkButton(master = settingsFrame, text="Exit", 
                                  command= lambda : self.returnToMenu(settingsFrame), width = 70, height = 15)
        settingsFrame.leaveButton.place(relx = 0.5, rely = 0.9, anchor = CENTER)

        return
    
    def returnToMenu(self, previousFrame):
        self.frameIndex = 0
        self.clearFrame(previousFrame)
        self.setupMenuFrame()

    def closeProgram(self):
        self.scheduler.setRunFlag(False)

        if self.video != None:
            self.video.exitVideo()

        if(self.frameIndex == 0):
            self.checkBoxStatus.deselect()
            self.checkBoxStatus.configure(text="Progam Off")

        try:
            self.scheduler.cancelQueue()
        except:
            pass
        return

    def exit(self):
        self.userData.saveUserData()
        if not self.scheduler.getRunFlag():
            self.closeProgram()
        sys.exit()

    def launch(self):

        def videoThread():
            self.scheduler.setLaunchTimeRange(self.launchTimeRange)
            self.scheduler.randomVideosEvent(self.userData.getPathToFolder(), self.userData.getMediaType())

        if not self.scheduler.getRunFlag() and self.pathValid:
            winAccess = win.WindowsAccess()
            winAccess.minimizeWindow(self.windowTitle)

            self.checkBoxStatus.select()
            self.checkBoxStatus.configure(text="Progam On")

            t1=Thread(target=videoThread)
            t1.daemon = True
            t1.start()

            self.scheduler.setRunFlag(True)
    
    def clearFrame(self, frame: CTkFrame):
        for widget in frame.winfo_children():
            widget.destroy()
            
        frame.pack_forget()

gui = GUI() 