import os 
import sys

import webbrowser

import UserData as user
import Schedule as sch
import WindowsAccess as win

from customtkinter import *
from tkinter import *

from threading import *
#qqqqqq
class GUI:
    
    def __init__(self) -> None:
        self.userData = user.UserData(path = "Enter Your Folder Path Here")
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

        label = CTkLabel(menuFrame, width = 100, text = "Input max time between videos", fg_color = ("white", "#1c6ba3"), corner_radius=8)
        label.pack(side = BOTTOM)

        #time input
        bottomFrame = CTkFrame(menuFrame, height = 40, width = 350, fg_color = "#2b2b2b", corner_radius=5)
        bottomFrame.pack(side = BOTTOM)

        self.scale1 = CTkSlider(bottomFrame, from_= 0, to=5, orientation="horizontal", number_of_steps = 20)
        self.scale1.set(self.userData.getTimeRange())
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
        self.scheduler.setRunFlag(False)

        if self.video != None:
            self.video.exitVideo()

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
            self.scheduler.randomVideosEvent(self.userData.getPathToFolder())

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