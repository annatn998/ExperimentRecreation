import random
from random import randint
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PIL import Image
from PyQt5.QtMultimedia import *
import sys
import pygame
soundEffect = '487195__nicknamelarry__typewriter-cartoon.wav'



###################################################################################
###################################################################################
#This folder holds certain functions and classes that are imported into the main file so that I can call upon them later

#creating a class for a clickable label so that the doors in my experiment can be clicked
class ClickableLabel (QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

#creating a class keyboard widget so that I can have some pages linked to the keyboard during certain parts of the experiment.
class KeyboardWidget(QWidget):
    keyPressed = pyqtSignal(str)
    def keyPressEvent(self,keyEvent):
        self.keyPressed.emit(keyEvent.text())

#I wanted a flashing label at the end of the experiment when showing the amount of money won
class ColoredLabel(QLabel):
    def setColor(self,colorString):
        self.setAutoFillBackground(True)
        myPalette = self.palette()
        myPalette.setColor(QPalette.Window, QColor(colorString))
        self.setPalette(myPalette)
    def blink(self,color1,color2):
        self. blinkColor1 = color1
        self.blinkColor2 = color2
        self.currentColor = color1
        self.blinkTimer = QTimer()
        self.blinkTimer.timeout.connect(self.onBlink)
        self.blinkTimer.start(500)
    def onBlink(self):
        if self.currentColor == self.blinkColor1:
            self.currentColor = self.blinkColor2
        else:
            self.currentColor = self.blinkColor1
        self.setColor(self.currentColor)


###################################################################################
###################################################################################
#this will pick half of the trials randomly to show a win label to and then the other half of the trials will shown
#using this predetermined pseudorandom list of results the appropirate label for the result will show up when the participant picks a door

def pseudorandomAssignment(N, prop):
    NumberOfTrials = N
    proportion = prop
    N_pos = int(N * prop)
    N_neg = N - N_pos
    listName = []

    for trials in range(1, N+1):
        randomTrial = (randint(0, N+1))
        if randomTrial <= N_pos:
            results = 'pos'
        elif randomTrial >= N_neg:
            results = 'neg'
        listName.append(results)
    return(listName)


#this is the function using the pseudorandomAssignment
def results(window):
    if window.preDeterminedResults[window.trialNumber - 1] == 'pos':  # subtracting the 1 so that the trials do not go out of range
        window.lblWin.show()
        window.feedBack = 'pos'
        window.moneyWon += 0.05 #making sure that I have the money that they will win added up
    elif window.preDeterminedResults[window.trialNumber - 1] == 'neg':
        window.lblLose.show()
        window.feedBack = 'neg'

###################################################################################
###################################################################################
#creating a button so that people can click and it will attach a certain function for later on in the code
#this is linked to the keyboard widget class

def button(lbl,function,function2=True,function3=True,function4=True):
    button = KeyboardWidget(lbl)
    button.setGeometry(200,40,500,500)
    button.setFocus()
    button.keyPressed.connect(function)
    button.keyPressed.connect(function2)
    button.keyPressed.connect(function3)
    button.keyPressed.connect(function4)



###################################################################################
###################################################################################
#because only one part of the geometry changes for the door but the rest of the qualities stay the same I can create a function
#that allows me to just put in the door name and the desired position change to create all 4 doors
#this is linked to the clickable label class

def Door(lable,int,page,function):
    label = ClickableLabel(page)
    pixmap = QPixmap('door.png')
    label.setPixmap(pixmap)
    label.setGeometry(int,100,111,161)
    label.setScaledContents(True)
    label.clicked.connect(function)

#this is so that I can create the flashing label in the main file
#this is linked to the colored label class
def lblColor(window,text,x,y,h,w):
    lblColor = ColoredLabel(window)
    lblColor.setText(text) #So that I can set the text in the main file
    lblColor.setGeometry(x,y,h,w)
    lblColor.setColor('pink') #setting the original color
    lblColor.blink('pink','purple')
    lblColor.setStyleSheet("font: 30pt Papyrus") #I like papyrus

###################################################################################
###################################################################################
#function to check for demographics

def nameCheck(window):
    if window.name == '':
        window.lblError.show()
        return False
    else:
        return True
def GenderCheck(window):
    if window.gender == '':
        return False
    else:
        return True
def educationCheck(window):
    if window.education == '':
        window.lblError.show()
        return False
    else:
        return True
def studyCheck(window):
    if window.study == '':
        window.lblError.show()
        return False
    else:
        return True

def ageCheck(window):
    if window.age == 0:
        return False
    else:
        return True

#this function will actually write all of the participant's demographics into the CSV file
def writeDemographicInfo(fileName,window):
    fileName.write(str(window.name) + ',' + str(window.age) + ',' + str(window.gender) + ',' + str(window.education) + ',' + str(
        window.student) + ',' + str(window.study) + '\n')


###################################################################################
###################################################################################
#creating a function to play sound so that I can link it to the animation
#will call this only when the last trial has ended
def playTyperWriterSound():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(soundEffect)
    pygame.mixer.music.play(0)


