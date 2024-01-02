import os
import csv

class UserData:
    def __init__(self, path: str = "", time: float = 2.50) -> None:

        self.curDir = os.getcwd()

        self.pathToFolder = path
        self.timeRange = time
        self.userDataStorage = [self.pathToFolder, self.timeRange]

        pass 

    def getCurrentDir(self):
        return self.curDir

    def initSaveFile(self):
        if not os.path.isfile(self.curDir + "\\save.csv"):
            open(self.curDir + "\\save.csv", "w", newline='')

    def getPathToFolder(self):
        return self.pathToFolder
    
    def setPathToFolder(self, path: str):
        self.pathToFolder = path
        self.userDataStorage[0] = self.pathToFolder

    def getTimeRange(self):
        return self.timeRange
    
    def setTimeRange(self, time: float):
        self.timeRange = time
        self.userDataStorage[1] = self.timeRange

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
            writer.writerow(self.userDataStorage)