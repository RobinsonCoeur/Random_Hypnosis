import os
import csv
import json 

from customtkinter import *
from customtkinter import filedialog

class UserData:
    def __init__(self, path: str = "Enter Your Folder Path Here", time: float = 2.50, maxTime: int = 5, mediaType: str = "both", mode: str = "Soft", videoLinks: list = []) -> None:

        self.curDir = os.getcwd()

        self.pathToFolder = path
        self.timeRange = time
        self.maxTime = maxTime
        self.mediaType = mediaType
        self.mode = mode
        self.videoLinks = videoLinks

        pass 

    def setVideoLinks(self, videoLinks:list):
        self.videoLinks = videoLinks
        self.saveLinks()
        pass

    def getVideoLinks(self):
        return self.videoLinks

    def setMediaType(self, type):
        self.mediaType = type
        pass
    
    def getMediaType(self):
        return self.mediaType

    def setMaxTime(self, time):
        self.maxTime = time

    def getMaxTime(self):
        return self.maxTime

    def getCurrentDir(self):
        return self.curDir
    
    def getMode(self):
        return self.mode
    
    def setMode(self, inMode):
        self.mode = inMode
        return

    def initSaveFile(self):
        if not os.path.isfile(self.curDir + "\\save.csv"):
            open(self.curDir + "\\userdata\\save.csv", "w", newline='')

        if not os.path.isfile(self.curDir + "\\links.csv"):
            open(self.curDir + "\\userdata\\links.csv", "w", newline='')

    def getPathToFolder(self):
        return self.pathToFolder
    
    def setPathToFolder(self, path: str):
        self.pathToFolder = path

    def getTimeRange(self):
        return self.timeRange
    
    def setTimeRange(self, time: float):
        self.timeRange = time

    def loadUserData(self):
        with open(self.curDir+ "\\userdata\\save.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                userDataStorage = row

            try:
                self.setPathToFolder(userDataStorage[0])
                self.setTimeRange(float(userDataStorage[1]))
                self.setMaxTime(int(userDataStorage[2]))
                self.setMediaType(userDataStorage[3])
                self.setMode(userDataStorage[4])
            except:
                pass

        with open(self.curDir+ "\\userdata\\links.csv", "r") as f:
                reader = csv.reader(f)
                linksList = []
                for row in reader:
                    for item in row:
                        linksList.append(item)
                self.setVideoLinks(linksList)


    def saveUserData(self):
        with open("userdata/save.csv", "w", newline='') as f:
            writer = csv.writer(f)
            userDataStorage = [self.pathToFolder, self.timeRange, self.maxTime, self.mediaType, self.mode]
            writer.writerow(userDataStorage)

        self.saveLinks() 

    def saveLinks(self):
        with open("userdata/links.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.videoLinks)
        pass

    def saveLinkList(self, linkList, saveFileName : str):
        fileName = saveFileName + ".csv"
        with open(fileName, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(linkList)
        pass
    
    def loadLinkList(self, root : CTk):
        folderPath = filedialog.askopenfilename(title = "Select a File")
        with open(folderPath, "r") as f:
            reader = csv.reader(f)
            linksList = []
            for row in reader:
                for item in row:
                    linksList.append(item)
        return linksList
