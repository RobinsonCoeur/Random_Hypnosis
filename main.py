import os 
import keyboard
import random

import webbrowser

import vlc

import sched
import time

from customtkinter import *
from tkinter import *

from threading import *

class GUI:
    
    def __init__(self):
        self.root = CTk()
        self.root.title("Playlist Creator")
        self.root.geometry('380x420')

        self.mediaPlayer = vlc.MediaPlayer()

        self.launchTimeRange =  3600 #in seconds
        
        self.setupMenuFrame()

        self.root.after(50, self.checkFrameConditions) 
        self.root.mainloop()
    
    def loadVlcDownloadPage(self):
        webbrowser.open('https://get.videolan.org/vlc/3.0.11/win64/vlc-3.0.11-win64.exe') 

    def createEntryInFrame(self, frame: CTkFrame, text: str = "", width: int = 100):
        entry = CTkEntry(frame, width = width)
        entry.insert(1, text) 
        entry.pack()
        
        return entry
    
    def checkFrameConditions(self):
        
        self.scaleValue.configure(text = str(self.scale1.get()) + " hours")
        self.root.after(50, self.checkFrameConditions)

        return

    def setupMenuFrame(self) -> None:
        menuFrame = CTkFrame(self.root)
        set_appearance_mode("dark")
        menuFrame.pack(side="top", expand=True, fill="both")

        linkEntry = self.createEntryInFrame(menuFrame, '"Path to your video files"', 210)
        
        menuFrame.buttonLaunch = CTkButton(master = menuFrame, text="Launch !", 
                                  command= lambda : self.launch(linkEntry))
        menuFrame.buttonLaunch.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        menuFrame.buttonVLC = CTkButton(master = menuFrame, text="Download VLC ?", 
                                  command= lambda : self.loadVlcDownloadPage())
        menuFrame.buttonVLC.place(relx = 0.5, rely = 0.6, anchor = CENTER)

        label = CTkLabel(menuFrame, width = 100, text = "Input max time without video", fg_color = ("white", "#1c6ba3"), corner_radius=8)
        label.pack(side = BOTTOM)

        #time input
        bottomFrame = CTkFrame(menuFrame, height = 40, width = 350, fg_color = "#2b2b2b", corner_radius=5)
        bottomFrame.pack(side = BOTTOM)

        self.scale1 = CTkSlider(bottomFrame, from_= 0, to=10, orientation="horizontal", number_of_steps = 20)
        self.scale1.place(relx = 0.47, rely = 0.5, anchor = CENTER)

        self.scaleValue = CTkLabel(bottomFrame, width = 10, text = "0", fg_color = ("white", "#1c6ba3"), corner_radius= 5)
        self.scaleValue.place(relx = 0.90, rely = 0.5, anchor = CENTER)
        
        return

    def launch(self, linkEntry):
        filepath = linkEntry.get()
        self.root.destroy()
        self.randomEvent(filepath)

    def video(self, file):
        self.mediaPlayer.toggle_fullscreen()
        media = vlc.Media(file)
        self.mediaPlayer.set_media(media)
 
        def videoThread():
            self.mediaPlayer.play()
            time.sleep(1)

        t1=Thread(target=videoThread)
        t1.start()

        def exitThread():
            while True:
                if keyboard.is_pressed("a"):
                    self.mediaPlayer.stop()
                    break
            
        t2 = Thread(target = exitThread)
        t2.start()

    def randomEvent(self, folderPath):
        eventSchedule = sched.scheduler(time.time, time.sleep)

        def loadVideo():
            files = os.listdir(folderPath)
            chosenFile = files[random.randint(0, len(files)-1)]

            self.video(r"{}".format(folderPath + "\\" + chosenFile))
            time.sleep(1)

            delay = self.mediaPlayer.get_length()/1000 - 1

            eventSchedule.enter(random.randint(delay, self.launchTimeRange), 1, loadVideo)

        eventSchedule.enter(30, 1, loadVideo)
        eventSchedule.run()    
    
    def clearFrame(self, frame: CTkFrame):
        for widget in frame.winfo_children():
            widget.destroy()
            
        frame.pack_forget()

    ##TESTS##
    def testVideoLoading(self):
        self.video(r"F:\Users\cyriletjulia\Documents\Loïc\Musique création\videos\boobs.mp4")

gui = GUI() 