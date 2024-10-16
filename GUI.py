import os 
import sys

import webbrowser

import UserData as user
import Schedule as sch
import WindowsAccess as win

from customtkinter import *
from tkinter import *

from threading import *

class GUI:
    
    def __init__(self) -> None:
        self.windowAccess = win.WindowsAccess()
        self.windowAccess.showTaskBar()

        self.userData = user.UserData()
        self.userData.initSaveFile()
        self.userData.loadUserData()
        self.linkList = self.userData.getVideoLinks()

        self.bufferPath = ""
        self.bufferTimerValue = 0

        self.scheduler = sch.Schedule()
        self.video = None

        self.linkFramesList = []

        self.pathValid = False
        self.onLaunchFlag = True

        self.root = CTk()
        self.windowTitle = "Hypnosis Computer Virus"
        self.root.after(201, lambda :self.root.iconbitmap(self.userData.getCurrentDir() + '\\myIcon.ico'))
        self.root.title(self.windowTitle)
        self.root.geometry('380x620')
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
        if (inMin <= 9 and sliderValue > 0.098):
            inMin = int(str(inMin) + "0")
        self.scaleValue.configure(text = hrs + " hr and " + str(inMin*60/100).split(".")[0] + " min")

        return

    def checkFrameConditions(self):
        if (self.frameIndex == 0):
            pathToFiles = self.linkEntry.get()
            self.verifyPathValidity(pathToFiles)

            sliderValue = self.scale1.get()

            if self.onLaunchFlag or sliderValue != self.bufferTimerValue:
                self.bufferTimerValue = sliderValue
                self.userData.setTimeRange(sliderValue)
                self.updateSliderLabel(sliderValue)

            self.launchTimeRange = int(sliderValue*60*60) + 1

        if (self.frameIndex == 1):
            entry = self.maxTimeEntry.get()
            if entry != '' and int(entry) >= 1:
                self.userData.setMaxTime(int(entry))

        self.root.after(50, self.checkFrameConditions)

        return

    def setupOptionsGrid(self, masterFrame):
        optionsFrame = CTkFrame(masterFrame, height = 40, width = 400, fg_color = "#2b2b2b", corner_radius=5)
        optionsFrame.pack(side = TOP)

        optionsFrame.buttonSettings = CTkButton(master = optionsFrame, text="Settings", 
                                  command= lambda : self.setupSettingsFrame(optionsFrame.master), width = 100, height = 19)
        optionsFrame.buttonSettings.place(relx = 0.15, rely = 0.5, anchor = CENTER)

        optionsFrame.buttonLinks = CTkButton(master = optionsFrame, text="Videos from Hypnotube", command= lambda : self.setupAddLinkFrame(optionsFrame.master), width = 150, height = 19)
        optionsFrame.buttonLinks.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        pass

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
        maxLabel.place(relx = 0.5, rely = 0.45, anchor = CENTER)

        self.maxTimeEntry = self.createEntryInFrame(settingsFrame, str(self.userData.getMaxTime()), 50)
        self.maxTimeEntry.place(relx = 0.5, rely = 0.55, anchor = CENTER)

        #media type
        mediaChoiceFrame = CTkFrame(settingsFrame, height = 150, width = 300, fg_color = "#2b2b2b", corner_radius=5)
        mediaChoiceFrame.pack(side = TOP)

        def checkboxVideoEvent():
            if checkboxVideo.get() == "on":
                checkboxInternet.deselect()
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
                checkboxInternet.deselect()
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

        def checkboxOnlineEvent():
            if checkboxInternet.get() == "on":
                self.userData.setMediaType("online")
                checkboxVideo.deselect()
                checkboxAudio.deselect()

            pass

        media = self.userData.getMediaType()

        mediaLabel = CTkLabel(mediaChoiceFrame, width = 100, text = "Select what you want to play", fg_color = ("white", self.labelBgColor), corner_radius=self.labelRad)
        mediaLabel.place(relx = 0.5, rely = 0.2, anchor = CENTER)

        check_var = StringVar(value="on")
        checkboxVideo = CTkCheckBox(mediaChoiceFrame, text="Video", command=checkboxVideoEvent,
                                     variable=check_var, onvalue="on", offvalue="off", checkbox_width = 21, checkbox_height = 21)
        checkboxVideo.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        if media == "audio" or media == "none"or media == "online":
            checkboxVideo.deselect()
        
        check_var = StringVar(value="on")
        checkboxAudio = CTkCheckBox(mediaChoiceFrame, text="Audio", command=checkboxAudioEvent,
                                     variable=check_var, onvalue="on", offvalue="off", checkbox_width = 21, checkbox_height = 21)
        checkboxAudio.place(relx = 0.5, rely = 0.7, anchor = CENTER)

        if media == "video" or media == "none" or media == "online":
            checkboxAudio.deselect()

        check_var = StringVar(value="on")
        checkboxInternet = CTkCheckBox(mediaChoiceFrame, text="Hypnotube Link", command=checkboxOnlineEvent,
                                     variable=check_var, onvalue="on", offvalue="off", checkbox_width = 21, checkbox_height = 21)
        checkboxInternet.place(relx = 0.5, rely = 0.9, anchor = CENTER)

        if media == "video" or media == "none" or media == "both" or media == "audio":
            checkboxInternet.deselect()

        settingsFrame.leaveButton = CTkButton(master = settingsFrame, text="Exit", 
                                  command= lambda : self.returnToMenu(settingsFrame), width = 70, height = 15)
        settingsFrame.leaveButton.place(relx = 0.5, rely = 0.9, anchor = CENTER)

        #dangerosity mode

        dangerChoiceFrame = CTkFrame(settingsFrame, height = 100, width = 300, fg_color = "#2b2b2b", corner_radius=5)
        dangerChoiceFrame.place(relx = 0.5, rely = 0.7, anchor = CENTER)

        maxLabel = CTkLabel(dangerChoiceFrame, width = 100, text = "Select Dangerosity Mode", fg_color = ("white", self.labelBgColor), corner_radius=self.labelRad)
        maxLabel.place(relx = 0.5, rely = 0.35, anchor = CENTER)

        comboboxVar = StringVar(value=self.userData.getMode())  # set initial value

        def comboboxCallback(choice):
            self.userData.setMode(choice)
            return

        self.modeWidget = CTkComboBox(dangerChoiceFrame, values=["Soft", "No Escape"], command=comboboxCallback, variable=comboboxVar)
        self.modeWidget.place(relx = 0.5, rely = 0.7, anchor = CENTER)

        return
    

    def setupAddLinkFrame(self, previousFrame):
        def extractTitleFromLink(link:str):
            linkListed = link.split("/")
            
            if "channels" in linkListed:
                title = linkListed[-2] + " category"
            else:
                titleRaw = linkListed[-1]
                titleList = titleRaw.split("-")
                title = ""

                for word in titleList:
                    if not word.split(".")[0].isdigit():
                        title = title + word
                        title += " "

            return title

        def addTitleWidget(position: int, title: str, link: str, parentFrame: CTkFrame):
            localFrame = CTkFrame(parentFrame, height = 50, width = 300, fg_color = "#2b2b2b", corner_radius=5)
            localFrame.place(relx = 0.5, rely = position*0.1+0.05, anchor = CENTER)

            linkLabel = CTkLabel(localFrame, width = 200, text = title, fg_color = ("white", self.labelBgColor), corner_radius=self.labelRad)
            linkLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)

            buttonAddLink = CTkButton(master = localFrame, text="-", 
                                  command= lambda : removeLink(localFrame, link), width = 25, height = 20, fg_color = ("white", self.labelBgColor))
            buttonAddLink.place(relx = 0.9, rely = 0.5, anchor = CENTER)

            self.linkFramesList.append(localFrame)
            
            pass

        def addLinkFromtextEntry(parentFrame: CTkFrame):
            link = linkLoadEntry.get().replace('"', "")
            addLink(link, parentFrame)
            pass

        def addLink(link, parentFrame):
            if len(self.linkList) < 9 and link not in self.linkList:
                title = extractTitleFromLink(link)
                addTitleWidget(len(self.linkList)+1, title, link, parentFrame)

                self.linkList.append(link)
            pass

        def updateLinksFramePosition():
            for i in range(0, len(self.linkFramesList)):
                self.linkFramesList[i].place(relx = 0.5, rely = (i+1)*0.1+0.05, anchor = CENTER)

        def removeLink(frame:CTkFrame, link:str):
            frame.destroy()
            self.linkList.remove(link)
            self.linkFramesList.remove(frame)
            updateLinksFramePosition()
            pass

        def clearLinkFrame(parentFrame : CTkFrame):
            for widget in parentFrame.winfo_children():
                widget.destroy()
            self.linkList = []
            pass

        def loadLinkList(parentFrame : Frame):
            linkList = self.userData.loadLinkList(self.root)

            clearLinkFrame(parentFrame)

            for link in linkList:
                addLink(link, parentFrame)
        pass

        self.frameIndex = 2
        self.clearFrame(previousFrame)
            
        linkFrame = CTkFrame(self.root)
        set_appearance_mode("dark")
        linkFrame.pack(side="top", expand=True, fill="both")  

        linksSavedFrame = CTkFrame(linkFrame, height = 400, width = 300, fg_color = "#2b2b2b", corner_radius=5)
        linksSavedFrame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        for i in range(0, len(self.linkList)):
            link = self.linkList[i]
            title = extractTitleFromLink(link)
            addTitleWidget(i+1, title, link, linksSavedFrame)

        #link entry
        linkLoadEntry = self.createEntryInFrame(linkFrame, "Enter your video or category link here", 225)
        linkLoadEntry.place(relx = 0.5, rely = 0.05, anchor = CENTER)

        buttonAddLink = CTkButton(master = linkFrame, text="Add", 
                                  command= lambda : addLinkFromtextEntry(linksSavedFrame), width = 50)
        buttonAddLink.place(relx = 0.87, rely = 0.05, anchor = CENTER)

        buttonSaveLinkList = CTkButton(master = linkFrame, text="Save List", 
                                  command= lambda : self.setupFrameSaveLinkList(linkFrame))
        buttonSaveLinkList.place(relx = 0.7, rely = 0.87, anchor = CENTER)

        buttonLoadLinkList = CTkButton(master = linkFrame, text="Load List", 
                                  command= lambda : loadLinkList(linksSavedFrame))
        buttonLoadLinkList.place(relx = 0.3, rely = 0.87, anchor = CENTER)

        buttonRegister = CTkButton(master = linkFrame, text="Back", 
                                  command= lambda : self.registerVideoLinks(linkFrame))
        buttonRegister.place(relx = 0.5, rely = 0.95, anchor = CENTER)

        pass

    def setupFrameSaveLinkList(self, previousFrame):
        def saveLinkList(parentFrame):
            self.userData.saveLinkList(self.linkList, fileName.get())
            self.setupAddLinkFrame(parentFrame)
            pass

        self.clearFrame(previousFrame)  

        saveLinkFrame = CTkFrame(self.root)
        set_appearance_mode("dark")
        saveLinkFrame.pack(side="top", expand=True, fill="both")  

        savedFrame = CTkFrame(saveLinkFrame, height = 400, width = 300, fg_color = "#2b2b2b", corner_radius=5)
        savedFrame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        fileName = self.createEntryInFrame(savedFrame, "Enter your save file name here", 210)
        fileName.place(relx = 0.5, rely = 0.05, anchor = CENTER)

        buttonRegister = CTkButton(master = saveLinkFrame, text="Save", 
                                  command= lambda : saveLinkList(saveLinkFrame))
        buttonRegister.place(relx = 0.5, rely = 0.95, anchor = CENTER)

        pass

    def registerVideoLinks(self, previousFrame):
        self.returnToMenu(previousFrame)
        self.userData.setVideoLinks(self.linkList)
        pass

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
            self.scheduler.randomVideosEvent(self.userData.getPathToFolder(), self.userData.getMediaType(), self.userData.getMode(), self.userData.getVideoLinks())

        if not self.scheduler.getRunFlag():
            if self.userData.getMediaType() != "online" and self.pathValid or self.userData.getMediaType() == "online":
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