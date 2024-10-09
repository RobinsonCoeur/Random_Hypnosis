import requests
from bs4 import BeautifulSoup

class HypnotubeAccess():
    def __init__(self) -> None:
        pass

    def getCategoryVideosList(self, categoryLink):
        #takes vids from 1st page with setting "newest"
        page = requests.get(categoryLink)
        htmlData = BeautifulSoup(page.content, "html.parser")

        videoLinks = []

        videosSpace = htmlData.find_all("div", class_ = "item-col col")
        for item in videosSpace:
            try:
                link = item.find_all("a")[0]["href"]
                videoLinks.append(link)
            except:
                print("no link")

        return videoLinks
    
    def extractVideoFromLink(self, link: str):
        file = ""
        #extract file like https://cdn.hypnotube.com/videos/5/f/d/5/d/5fd5d34293d6a.mp4 from link html
        
        page = requests.get(link)
        htmlData = BeautifulSoup(page.content, "html.parser")

        videoSpace = htmlData.find_all("div", class_ = "inner-stage")
        for item in videoSpace:
            file = item.find_all("source")[0]["src"]
                    
        return file
