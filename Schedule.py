import sched
import time
import random
import os 

import Audio as aud
import Video as vid
import UserData as user
import HypnotubeAccess as acchyp

class Schedule:
    def __init__(self) -> None:

        self.hypnotubeAccess = acchyp.HypnotubeAccess()

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

    def getRunFlag(self):
        return self.run

    def randomVideosEvent(self, folderPath: str, mediaType: str = "both", mode: str = "Soft", linksList: list = []):
        def scrapFolderForVideos(filesList, additionalPath = ""):
            if additionalPath == "":
                path = folderPath
            else:
                path = r"{}".format(folderPath + "\\" + additionalPath)

            files = os.listdir(path)
            for file in files:
                if len(file.split(".")) == 1:

                    if additionalPath == "":
                        filePath = file
                    else:
                        filePath = r"{}".format(additionalPath + "\\" + file)
                        
                    scrapFolderForVideos(filesList, filePath)
                else:
                    filesList.append(file)
            pass

        def loadContent():
            if not mediaType == "online":
                filesList = []
                scrapFolderForVideos(filesList)
                print(filesList)
                chosenFile = filesList[random.randint(0, len(filesList)-1)]
                path = r"{}".format(folderPath + "\\" + chosenFile)

                if "mp3" in chosenFile.split(".") and (mediaType == "audio" or mediaType == "both"):
                    audio = aud.Audio(path)
                    audio.launchAudio()
                    exitType = audio.getExitType()

                elif mediaType == "video" or mediaType == "both":
                    video = vid.Video(path, mode)
                    video.launchVideo()
                    exitType = video.getExitType()
                else:
                    exitType = 3

            else:
                bufferAddedLinks = []
                for link in linksList:
                    linkListed = link.split("/")
                    if "channels" in linkListed:
                        categoryVideoLinks = self.hypnotubeAccess.getCategoryVideosList(link)
                        for link in categoryVideoLinks:
                            bufferAddedLinks.append(link)

                for link in bufferAddedLinks:
                    linksList.append(link)

                path = linksList[random.randint(0, len(linksList)-1)]
            
                if mediaType == "online":
                    video = vid.Video(path, mode, localFile=False)
                    video.launchVideo()
                    exitType = video.getExitType()
                else:
                    exitType = 3

            if self.run:
                if exitType == 1:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadContent)
                if exitType == 2:
                    self.currentIdInQueue = self.eventSchedule.enter(random.randint(self.safetyTime, self.launchTimeRange+self.safetyTime), 1, loadContent)
        
        self.currentIdInQueue = self.eventSchedule.enter(random.randint(1, self.launchTimeRange), 1, loadContent)
        self.eventSchedule.run()

