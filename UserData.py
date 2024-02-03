import os
import csv

class UserData:
    def __init__(self, path: str = "Enter Your Folder Path Here", time: float = 2.50, maxTime: int = 5, mediaType: str = "both", mode: str = "Soft") -> None:

        self.curDir = os.getcwd()

        self.pathToFolder = path
        self.timeRange = time
        self.maxTime = maxTime
        self.mediaType = mediaType
        self.mode = mode

        pass 

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
            open(self.curDir + "\\save.csv", "w", newline='')

    def getPathToFolder(self):
        return self.pathToFolder
    
    def setPathToFolder(self, path: str):
        self.pathToFolder = path

    def getTimeRange(self):
        return self.timeRange
    
    def setTimeRange(self, time: float):
        self.timeRange = time

    def loadUserData(self):
        with open(self.curDir+ "\\save.csv", "r") as f:
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

    def saveUserData(self):
        with open("save.csv", "w", newline='') as f:
            writer = csv.writer(f)
            userDataStorage = [self.pathToFolder, self.timeRange, self.maxTime, self.mediaType, self.mode]
            writer.writerow(userDataStorage)