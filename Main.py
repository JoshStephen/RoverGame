from RoverImage import RoverImage
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkFont

##See if fileDir roverImgs exists, if not create the fileDir and fill it with imgs
fileDir = '.\\roverImgs'
load_dotenv()
apiKey = os.getenv('NASA_KEY')
nasaRover = RoverImage(apiKey, fileDir)
if not os.path.isdir(fileDir):
    print(f'Dir not exist, making dir: {fileDir} \nThis make take awhile')
    os.mkdir(fileDir)
    nasaRover.imgDownLoader('curio',nasaRover.getBetterRoverUrls('Curiosity', 3))
    nasaRover.imgDownLoader('oppy',nasaRover.getBetterRoverUrls('Opportunity', 3))
    nasaRover.imgDownLoader('spirit',nasaRover.getBetterRoverUrls('Spirit', 3))

else:
    print('Dir exists, loading game now')


###Gui Setup for game
window = tk.Tk()
window.title("Mars Rover guessing Game")

labelHead = tk.Label(window, text="Guess which rover took this photo", font= tkFont.Font(size=13))
labelHead.grid(row=1, column=0, columnspan=5, padx=20)

labelScore = tk.Label(window, text='Score: 0')
labelScore.grid(row=2, column=0, columnspan=5)

roverImg = Image.open('PlaceHolder_.png')
homeImg = ImageTk.PhotoImage(roverImg)
labelImg = tk.Label(window, image=homeImg)
labelImg.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

##Buttons
btnCurio = tk.Button(window, text='Curiosity', state=tk.DISABLED)
btnCurio.grid(row=5, column=1)

btnOppy = tk.Button(window, text='Opportunity', state=tk.DISABLED)
btnOppy.grid(row=5, column=2)

btnSpirit = tk.Button(window, text='Spirit', state=tk.DISABLED)
btnSpirit.grid(row=5, column=3)

btnStart = tk.Button(window, text='Start Game')
btnStart.grid(row=7, column=2, padx=10, pady=10)

roverButtons = []
roverButtons.extend((btnCurio, btnOppy, btnSpirit))

###Game Rules
gameScore = 0
gameTurns = 6
gameStart = False
imgToGuess = 'place_holder'
roverToGuess = 'Place_holder'

def newGame():

    ##Activates roverBtns
    for b in roverButtons:
        b['state'] = tk.NORMAL
    
    ##change the name of start btn and change the function it's bound to
    btnStart['text'] = 'Restart'
    btnStart['command'] = restart

    ##change Home image
    newImage()


##Checks if the guess is right
def guess(roverGuess):
    global gameScore, gameTurns
    #print('########' + roverGuess)

    if gameTurns > 0:
        if roverGuess.upper() == roverToGuess.upper():
            gameScore += 1
    else:
        #deactivate btns
        for b in roverButtons:
            b['state'] = tk.DISABLED

    gameTurns -= 1
    labelScore['text'] = f'Score: {gameScore}'
    newImage()

##get a new Image and rover to guess
img = 'image'
def newImage():
    global imgToGuess, roverToGuess, labelImg, img
    imgToGuess = nasaRover.imgRandRetriever()
    #print(imgToGuess)

    if 'curio' in imgToGuess:
        roverToGuess = 'Curiosity'
    elif 'oppy' in imgToGuess:
        roverToGuess = 'Opportunity'
    elif 'spirit' in imgToGuess:
        roverToGuess = 'spirit'

    #print(roverToGuess)

    img = ImageTk.PhotoImage(Image.open(imgToGuess))
    #print(f'img {img}')

    labelImg['image'] = img

##Restarts game to startup
def restart():
    global gameScore, gameTurns, imgToGuess, roverToGuess

    gameScore = 0
    gameTurns = 6
    imgToGuess = 'place_holder'
    roverToGuess = 'place_holder'
    
    #reset main img
    labelImg['image'] = homeImg
    #reset Score
    labelScore['text'] = f'Score: {gameScore}'

    #deactivate btns
    for b in roverButtons:
        b['state'] = tk.DISABLED

    #revert start btn
    btnStart['command'] = newGame

##Connect btns
btnStart['command'] = newGame
btnCurio['command']= lambda : guess('Curiosity')
btnOppy['command']= lambda : guess('Opportunity')
btnSpirit['command']= lambda : guess('Spirit')


window.mainloop()