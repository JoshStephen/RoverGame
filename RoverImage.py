from nasapy import Nasa
import random
import urllib.request
import os
from PIL import Image

#from dotenv.main import load_dotenv

'''
The RoverImage class has two atrributes
'''
class RoverImage:

    def __init__(self, apiKey, fileDir):
        self.nasa = Nasa(apiKey)
        self.fileDir = fileDir

    ##Method getRoverUrls returns a list of imgAmount img urls from a given roverName
    # This method selects imgs from the same page, causing imgs to be very similar.
    # Use getBetterRoverUrls is avoid imgs being similar.
    def getRoverUrls(self, roverName, imgAmount):
        roverImgList = []
        imgListLength = 0
        maxSol = 0

        if roverName.upper() == 'OPPORTUNITY':
            maxSol = 5352
        elif roverName.upper() == 'CURIOSITY':
            maxSol = 3169
        elif roverName.upper() == 'SPIRIT':
            maxSol = 2200

        while imgListLength == 0:
            solNum = random.randint(100, maxSol)
            roverImgList = self.nasa.mars_rover(sol=solNum, camera='NAVCAM', rover=roverName ,page=1)
            imgListLength = len(roverImgList)
            #print(solNum)
        
        imgUrlList = []
        for i in range(imgAmount):
            randImg=random.randint(0, len(roverImgList))
            imgUrlList.append(roverImgList[randImg]['img_src'])
            #print(f'Img found, ImgNumb:{randImg}')

        return imgUrlList

    ##Method getRoverUrls returns a list of imgAmount img urls from a given roverName
    # This method selects an img from a page and then searchers for another page before getting another img.
    # in theory this should cause imgs to be different from each other.
    # The downside of this solution is that more calls are being made to Nasa's api,
    # which I believe will slow down prefromance, I haven't proven this but it's juts my gut feeling
    ##an addition note, I am unable to avoid the "white dot" imgs. 
    # As I'm pretty sure the only way to avoid them is through img recognition software or
    # maybe through a clever algorithm that deterims how much of the img is white. 
    def getBetterRoverUrls(self, roverName, imgAmount):
        roverImgList = []
        imgUrlList = []
        maxSol = 0

        if roverName.upper() == 'OPPORTUNITY':
            maxSol = 5352
        elif roverName.upper() == 'CURIOSITY':
            maxSol = 3169
        elif roverName.upper() == 'SPIRIT':
            maxSol = 2200

        ##print(f'max sol: {maxSol}')

        for x in range(imgAmount):
            solNum=0
            imgListLength = 0
            while imgListLength == 0:
                solNum = random.randint(0, maxSol)
                roverImgList = self.nasa.mars_rover(sol=solNum, camera='NAVCAM', rover=roverName ,page=1)
                imgListLength = len(roverImgList)
                print(f'List Length :{imgListLength}')
                print(f'Sol Number :{solNum}')

                if imgListLength > 0:
                    randImg=random.randint(0, len(roverImgList)-1)
                    imgUrlList.append(roverImgList[randImg]['img_src'])
                    print(f'Img found, Img number:{randImg}')

        return imgUrlList

    ##Method imgDownLoader takes a roverName and a List of imgs 
    # and then downloads that list to the class's given file dir
    # the method will name each img based of the roverName and an assigned number
    def imgDownLoader(self, roverName, imgList):
        imgNum = 0
        for img in imgList:
            imgFile = f'{self.fileDir}\\{roverName}_{imgNum}.png'
            urllib.request.urlretrieve(img, imgFile)
            imgNum+=1
            ##Resize img to be within 500x500, 
            # if Img is larger than 500x500
            ##Images don't seem to be resized if the are smaller than 500x500 
            # not sure as to why, will fix this at a later time
            imgSizeCheck = Image.open(imgFile)
            imgSize = imgSizeCheck.size
            if  imgSize > (500, 500):
                imgSizeCheck.thumbnail((500, 500))
                imgSizeCheck.save(imgFile)
            elif imgSize < (500, 500):
                imgSizeCheck.resize((500, 500))
                imgSizeCheck.save(imgFile)
            
            print('Img Downloaded')
        print(f'Imgs downloaded for {roverName}')

    ##Method imgRandRetriever will pick a random img 
    # from the assigned file dir and return it
    def imgRandRetriever(self):
        randImg = random.choice(os.listdir(self.fileDir))
        return f'{self.fileDir}\\{randImg}'


##Testing

""" load_dotenv()
ApiKey = os.getenv("NASA_KEY")
rover = RoverImage(ApiKey, '.\\roverimgs')
print(rover.getBetterRoverUrls('Curiosity', 3))
##print(rover.imgRandRetriever()) """
