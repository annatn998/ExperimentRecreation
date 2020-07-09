import random
from random import randint
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from FunctionsHolder import *
from PyQt5.QtMultimedia import *
import sys
import pygame
soundEffect = '487195__nicknamelarry__typewriter-cartoon.wav'

################################################################################
################################################################################
#openning and linking the pyQt GUI to pycharm and then openning up the demographic csv file I created so that I can write in the particpant info


app = QApplication([])
window = uic.loadUi("GamblingTaskGUI.ui")
fileDemo = open('DemographicInfo.csv','a') #append because I created the titles on a different module


def nextPage(): #creating one function to call on whenever I want to turn to the next page put before everything because this is the first function called
    window.stackedWidget.setCurrentIndex(window.stackedWidget.currentIndex() + 1)

###################################################################################
###################################################################################
#below is a list of all the variables that will need to be created outside of the functions below

CSVFile = open('ParticipantInfo.csv','a')
window.student = ''
window.trialNumber = 0
window.doorNumber = []
window.moneyWon = 0
window.feedBack = ''
window.response = []
window.sentenceBuild = ''
window.n = 0
animatedSentence = "You have won: " #called animated sentence because it will be animated to have a typewriter effect

###################################################################################
###################################################################################

window.btnConsent.clicked.connect(nextPage)  #Only turning the page if the participant consents

###################################################################################
###################################################################################
#Part of the code used to sort out proporitons of win/loss results shown
#The function is called from the FunctionsHolder Page and it will randomize the results so that an almost equal proportion is shown for number of trials
#but in a random order so that participant does not know that the feedback is predetermined

window.preDeterminedResults = pseudorandomAssignment(4, 0.5) #0.5 because for when there is a large number of trials we want half to show positve
#and half to show negative reedback

###################################################################################
###################################################################################
#Create a function for list of items that need to be hidden at the beginning of the experiment so that
#I can use this function to hide the labels for every trial

def HiddenLabels():
    window.lblQuestion.hide()
    window.lblInstructions.hide()
    window.btnNo.hide()
    window.btnYes.hide()
    window.lblLose.hide()
    window.lblWin.hide()
    trials()


###################################################################################
###################################################################################
## These timers will be used to show stimuli for a certain period of time and to shift the page automatically
## after a certain amount of time has passed
#reason for large number of timers is because there are different functions called at the same time with different starting points that
#are required to make the program run in a certain order

NumberTimer = QTimer()
QuestionLabelTimer = QTimer()
HidePlusSignTimer = QTimer()
PlusIntervalTimer = QTimer()
HideFirstSignTimer = QTimer()
RewardTimer = QTimer()
PageTurnTimer = QTimer()

###################################################################################
###################################################################################
#This function will be used for the first fixation mark before the first trial. After 1 second the page will turn and the participant will no longer
#see the fixation mark. That is why both next page is timed to the timer as well as trials which will kick in other functions that are needed
#for subsequent parts of the experiment


def HideFirstSign():
    HideFirstSignTimer.timeout.connect(nextPage)
    HideFirstSignTimer.timeout.connect(trials)
    HideFirstSignTimer.start(1000)
    HideFirstSignTimer.setSingleShot(True)


###################################################################################
###################################################################################
#The following functions follow a set of logic similar to the HideFirstSign however slightly more complicated.
#I am using timers to turn the next page after a certain interval of time because I only
#want some things to be shown on the screen for a short amount of time. Therefore, within trials I have a pseudoRandom
#number being chosen and that becomes the trial condition. I set that trial condition to the door number and I change the
#text within the GUI to whatever the new trial number that was chosen.
#Then I set two timers within trials() that will call 2 separate functions at different times creating an interval of time between the pages
#that I want to turn i.e I connect HideNumber after 1 second and then showQuestionLabel at 2500 to create a time interval of the pages to be 1500
#using this way there will also be a small gap of blank space where the number is hidden as well so there is nothing on the screen
#The functions are put in order of when they are called below so that the system can be followed easier


def trials():
    if window.trialNumber != 0:
        window.stackedWidget.setCurrentIndex(4) #the first trial of the experiment calls upon trial a little differently so in order to move on
        #to other trials after the first one (0) we need to set the current index to 4 everytime trials() is called and it is not the first trial

    window.lblNumber.show()
    trialCondition = randint(1, 3) #we want the numbers 1,2 or 3, to show up on the screen randomly picked
    window.doorNumber.append(trialCondition)
    window.lblNumber.setText(str(window.doorNumber[-1]))
    window.doorNumberWrite = trialCondition

    #so that we don't have to have multiple labels within the GUI this way we can just set
    #one label and continue to set the text


    NumberTimer.timeout.connect(HideNumber)
    NumberTimer.start(1000)
    NumberTimer.setSingleShot(True)

    QuestionLabelTimer.timeout.connect(showQuestionLabel)
    QuestionLabelTimer.start(2500)  # use 2500 because we want the label to show 1500ms after the number is hidden
    QuestionLabelTimer.setSingleShot(True)

def HideNumber(): # just used to hide the number on the screen while the other labels are being shown
    window.lblNumber.hide()

def showQuestionLabel(): #this will show the labels that I want to ask the participant whether or not they believe that they will win this trial
    window.lblQuestion.show()
    window.lblInstructions.show()
    window.btnNo.show()
    window.btnYes.show()

def HidePlusSign(): #same pupose as the HideNumber(): function
    window.lblPlus.hide()
    HiddenLabels()

def yes():
    window.response.append('yes')
def no():
    window.response.append('no')

window.btnNo.clicked.connect(nextPage)
window.btnYes.clicked.connect(nextPage)
window.btnNo.clicked.connect(no)
window.btnYes.clicked.connect(yes)

button(window.pg1,HideFirstSign,HiddenLabels,nextPage,trials) #button called from FunctionsHolder called button because it makes any key
#on the keyboard into a button to turn the next page and call on the functions within the ().

def plusInterval(): #called plus interval because this function is in charge of creating the interval of time where the plus sign is shown
    #between each trial
    window.stackedWidget.setCurrentIndex(7) #page that the plus sign is on
    window.lblPlus.show()
    HidePlusSignTimer.timeout.connect(HidePlusSign)
    HidePlusSignTimer.start(1000) #this is 1000 because we want the screen to change after exactly 1 second of looking at fixation mark before each trial
    HidePlusSignTimer.setSingleShot(True) #all of the setSingleShots is so that the functions are not called repeatedly since some of them turn the page

def counter(): #called counter because it is the portion of the code that will count how many trials there are
    nextPage()
    window.trialNumber = window.trialNumber + 1 # adding to keep track of which trial number participant is on
    results(window)
    if window.trialNumber >1 and window.trialNumber <=3:
        #######writing CSV File in this function so that it writes before each trial

        CSVFile.write(str(window.trialNumber-1) + ',' + str(window.response[0]) + ',' + str(window.doorNumber[0])
                      + ',' + str(window.feedBack) + ',' + str(window.response[1]) + '\n')
        del window.response[0]
        del window.doorNumber[:3]

    if window.trialNumber <= 2: #you would change this number depending on the number of trials you wanted to do
        #to make the experiment go by quickly I'm only running 3 total trials 0 would be the first one
        PlusIntervalTimer.timeout.connect(plusInterval)
        PlusIntervalTimer.start(1000)
        PlusIntervalTimer.setSingleShot(True)
    else:
        NumberTimer.timeout.connect(FinalTrial)
        NumberTimer.start(1000)
        NumberTimer.setSingleShot(True)




def FinalTrial():
    window.stackedWidget.setCurrentIndex(8)
    playTyperWriterSound() #calling sound function to playtypewriter sound at the same time as the animation
    RewardTimer.timeout.connect(typewriterAnimation)
    RewardTimer.start(350) #This was time with the sound
    PageTurnTimer.timeout.connect(nextPage)
    PageTurnTimer.start(6000) #giving the typewriter time to write out the results
    PageTurnTimer.setSingleShot(True)




###################################################################################
###################################################################################
#Just a typewriter effect that will write out how much money the participant has won

def typewriterAnimation():
    if window.n < len(animatedSentence):
        window.sentenceBuild = window.sentenceBuild + animatedSentence[window.n]
        window.n+=1
        window.lblReward.setText(window.sentenceBuild)
    else:
        window.lblReward.setText(window.sentenceBuild + str(window.moneyWon))
    NumberTimer.stop() #we have to stop the timer here in the animation so that the typewriter sound effect is not replayed indefintely


###################################################################################
###################################################################################
##########using door function to create clickable doors for the experiment / function called from FunctionHolder

Door('Door1', 20, window.pg3, counter)
Door('Door2', 150, window.pg3, counter)
Door('Door3', 280, window.pg3, counter)
Door('Door4', 410, window.pg3, counter)


lblColor(window.pg8,"You're Done!",180,40,190,61) #calling my blinking label from Functions Holder to create a blinking label at the end


#Demographic Information Collection Portion of Code Below
################################################################################
################################################################################
#linking the demographics page to information that will be put into the CSV file
#calling on other demographic check functions so that the page doesn't move unless the participant answers all the question
# writing out information into CSV file for demographics
window.lblError.hide() #have to hide the label when the experiment begins and only show it if people have not filled out all portions
                        #of the demographic page


def CheckingAllDemographics():
    window.gender = ''
    window.age = window.ageBox.value()
    window.age = window.ageBox.value()
    window.education = window.educationBox.currentText()
    window.study = window.majorBox.text()
    window.name = window.nameBox.text()
    if window.btnFemale.isChecked():
        window.gender = 'Female'
    elif window.btnMale.isChecked():
        window.gender = 'Male'
    elif window.btnOther.isChecked():
        window.gender = 'other' + window.otherBox.text()
    #functions used to check the demographics is imported from functionsHolder
    if nameCheck(window) == True and ageCheck(window) and GenderCheck(window) == True and educationCheck(window) == True and studyCheck(window) == True:
        nextPage() #all of the demographic checking and information is imported from FunctionsHolder
        writeDemographicInfo(fileDemo,window)
window.btnDemo.clicked.connect(CheckingAllDemographics)



################################################################################
################################################################################
#End of Experiment

def windowClose():
    window.close() #function to call when the last button is clicked

window.btnFinish.clicked.connect(windowClose)


window.show()
app.exec()

