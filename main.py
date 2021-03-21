import PIL.ImageGrab
from PIL import ImageGrab, Image
from win32api import GetSystemMetrics
import pyautogui
import time
import random
import time
import os
import win32api
from Helpers.gtaKeyPress import *
import win32gui
import win32com
import win32con
import re

def isGreen(pixel):
    return (pixel[1] > (pixel[0] + DIFFERENCE_GREEN) and pixel[1] > (pixel[2] + DIFFERENCE_GREEN)) #and pixel[1] > 200)

def checkForGreen():
    while(True):
        img = PIL.ImageGrab.grab().load()
        for x in range(0,int(GetSystemMetrics(0)/3)):
            for y in range(int(GetSystemMetrics(1)/2),int(GetSystemMetrics(1)*3/4)):
                if isGreen(img[x,y]):
                    return img

def checkForMatchHelper(image1, image2):
    total = 0
    failure = 0
    for x in range(TOP_LEFT_X,TOP_RIGHT_X):
            for y in range(TOP_LEFT_Y,TOP_RIGHT_Y):
                if isGreen(image1[x,y]):
                    total += 1
                    if not isGreen(image2[x,y]):
                        failure += 1
                else:
                    if isGreen(image2[x,y]):
                        total += 1
                        failure += 1
    if (total == 0):
        return 0
    return (1- failure/total)


def checkForMatch(checkImage, images):
    percent = []
    for image in images:
        if image != 0:
            percent.append(checkForMatchHelper(image,checkImage))
        else:
            percent.append(0)
    return percent.index(max(percent)) + 1

def pressGivenKey(key):
    print("Pressing " + str(key))
    win32api.SetCursorPos((TOP_LEFT_X,TOP_LEFT_Y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,TOP_LEFT_X,TOP_LEFT_Y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,TOP_LEFT_X,TOP_LEFT_Y,0,0)
    # human random delay for pressing
    time.sleep(0.35 + random.randrange(1,200)/1000) 
    PressKey(getKeyCode(key))
    # human random delay for length of button press
    time.sleep(0.1 + random.randrange(1,100)/1000)
    ReleaseKey(getKeyCode(key)) 

def getKeyInput():
    key = input("Not seen, enter 1-9 to save:")
    try:
        key = int(key)
        if key > 0 and key < 10:
            return key
        else:
            print("invalid input not saving")  
    except:
        print("invalid input not saving")

def waitGreenDone():
    while(True):
        time.sleep(0.1)
        foundGreen = False
        img = PIL.ImageGrab.grab().load()
        for x in range(0,int(GetSystemMetrics(0)/3)):
            for y in range(int(GetSystemMetrics(1)/2),int(GetSystemMetrics(1)*3/4)):
                if isGreen(img[x,y]):
                    foundGreen = True
        if not foundGreen:
            return

def saveImage(image, number):
    image.save(os.getcwd() + "/images/imageFor" + str(number) + ".png", "JPEG")

def getSavedImage(number):
    image = Image.open(os.getcwd() + "/images/imageFor" + str(number) + ".png").load()
    return image

# top left = [58, 1037]
# bottom right = [371,1151]
#top left = 125 1093
#bottom right = 148, 1118
# 52.6 by 29.6
# 132 1106
#print(GetSystemMetrics(0)) #width
#print(GetSystemMetrics(1)) #height

def getImages():
    while(True):
        image = PIL.ImageGrab.grab()
        img = image.load()
        for x in range(0,int(GetSystemMetrics(0)/3)):
            for y in range(int(GetSystemMetrics(1)/2),int(GetSystemMetrics(1)*3/4)):
                if isGreen(img[x,y]):
                    return image

def loadImages():
    images = []
    for i in range(1,10):
        try:
            images.append(getSavedImage(i))
        except:
            print("Image not found for " + str(i))
            images.append(0)
    return images

def getCursorLocation():
    f  = open(os.getcwd() + "/images/cursorLocation.txt", "r")
    location = (int(f.readline()),int(f.readline()),int(f.readline()),int(f.readline()))
    f.close()
    return location

def doAutoFish():
    if (input("Do you need to set up? (y for yes):") == "y"):
        input("move cursor to top left of number")
        [x1,y1] = win32api.GetCursorPos()
        input("move cursor to bottom right of number")
        [x2,y2] = win32api.GetCursorPos()
        try:
            f = open(os.getcwd() + "/images/cursorLocation.txt", "w")
        except:
            f = open(os.getcwd() + "/images/cursorLocation.txt", "x")
        print(str(x1), file=f)
        print(str(x2), file=f)
        print(str(y1), file=f)
        print(str(y2), file=f)
        f.close()
        print(x1, y1)
        print(x2, y2)
        while(True):
            newImage = getImages()
            key = getKeyInput()
            if key != None:
                saveImage(newImage,key)
            waitGreenDone()
            print("Checking for catch")  
            time.sleep(4)
    else:
        images = loadImages()
        (TOP_LEFT_X,TOP_RIGHT_X,TOP_LEFT_Y,TOP_RIGHT_Y)=getCursorLocation()
        while(True):
            newImage = checkForGreen()
            print("Got one")
            key = checkForMatch(newImage, images)
            pressGivenKey(key)
            waitGreenDone()
            print("Checking for catch")  
            time.sleep(4)

DIFFERENCE_GREEN = 50 

TOP_LEFT_X = 0#125
TOP_LEFT_Y = 0#1093
TOP_RIGHT_X = 0#148
TOP_RIGHT_Y = 0#1118
# 1920 x 1080
# 2560 x 1440
# 126 x 1086
# 146 x 1133
# 120 x 1023
# 138 x 1059

if __name__ == '__main__':
    doAutoFish()
    '''
    (TOP_LEFT_X,TOP_RIGHT_X,TOP_LEFT_Y,TOP_RIGHT_Y)=getCursorLocation()
    print(TOP_LEFT_X*1920/GetSystemMetrics(0))
    print(TOP_LEFT_Y*1080/GetSystemMetrics(1))'''


    '''
    input("move cursor to top left of number")
    [x1,y1] = win32api.GetCursorPos()
    input("move cursor to bottom right of number")
    [x2,y2] = win32api.GetCursorPos()
    print(x1, y1)
    print(x2, y2)'''

    '''
    # red green blue
    red = (255,100,100)
    img = Image.open(os.getcwd() + "/imageFor2.png")
    image = img.load()
    (TOP_LEFT_X,TOP_RIGHT_X,TOP_LEFT_Y,TOP_RIGHT_Y)=getCursorLocation()
    for x in range(TOP_LEFT_X, TOP_RIGHT_X):
        image[x,TOP_LEFT_Y] = red
        image[x,TOP_RIGHT_Y] = red
    for y in range(TOP_LEFT_Y, TOP_RIGHT_Y):
        image[TOP_LEFT_X,y] = red
        image[TOP_RIGHT_X,y] = red
    img.save("test2.png")'''
