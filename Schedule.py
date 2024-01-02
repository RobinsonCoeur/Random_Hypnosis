import sched
import time
import random
import os 
import Video as vid

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

    def getVideoClass(self):
        return self.video

    def cancelQueue(self):
        self.eventSchedule.cancel(self.currentIdInQueue)

    def setRunFlag(self, state):
        self.run = state

    def randomVideosEvent(self, folderPath: str):
        def loadVideo():
            files = os.listdir(folderPath)
            chosenFile = files[random.randint(0, len(files)-1)]

            video = vid.Video(r"{}".format(folderPath + "\\" + chosenFile))
            video.launchVideo()
            exitType = video.getExitType()

            if self.run:
                if exitType == 1:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadVideo)
                if exitType == 2:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(self.safetyTime, self.launchTimeRange+self.safetyTime), 1, loadVideo)
        
        self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadVideo)
        self.eventSchedule.run()

