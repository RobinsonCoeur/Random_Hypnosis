import os
import csv

class UserData:
    def __init__(self, path: str = "", time: float = 2.50, browser: str = "chrome", maxTime: int = 5) -> None:

        self.curDir = os.getcwd()

        self.pathToFolder = path
        self.timeRange = time
        self.browser = browser
        self.maxTime = maxTime
        self.userDataStorage = [self.pathToFolder, self.timeRange, self.browser, self.maxTime]

        pass 

    def setMaxTime(self, time):
        self.maxTime = time
        self.userDataStorage[3] = time

    def getMaxTime(self):
        return self.maxTime

    def setUserBrowser(self, browser: str):
        self.browser = browser.lower()
        self.userDataStorage[2] = self.browser
    
    def getUserBrowser(self):
        return self.browser

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
                for i in range(0, len(row)):
                    self.userDataStorage[i] = row[i]

            self.setPathToFolder(self.userDataStorage[0])
            self.setTimeRange(float(self.userDataStorage[1]))
            self.setUserBrowser(self.userDataStorage[2])
            self.setMaxTime(int(self.userDataStorage[3]))

    def saveUserData(self):
        with open("save.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.userDataStorage)