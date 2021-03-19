import PIL.ImageGrab
from win32api import GetSystemMetrics
import pyautogui
import time
import random


import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# key codes https://wiki.nexusmods.com/index.php/DirectX_Scancodes_And_How_To_Use_Them
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
KEY_1 = 0x02
KEY_2 = 0x03
KEY_3 = 0x04
KEY_4 = 0x05
KEY_5 = 0x06
KEY_6 = 0x07
KEY_7 = 0x08
KEY_8 = 0x09
KEY_9 = 0x10

########################################################################
# Code from https://github.com/Sentdex/pygta5/blob/master/directkeys.py
#######################################################################
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
############################################################################################

def getKeyCode(key):
    switch = {
        1: KEY_1,
        2: KEY_2,
        3: KEY_3,
        4: KEY_4,
        5: KEY_5,
        6: KEY_6,
        7: KEY_7,
        8: KEY_8,
        9: KEY_9,
    }
    return switch.get(key)

def isGreen(pixel):
    return (pixel[1] > (pixel[0] + DIFFERENCE_GREEN) and pixel[1] > (pixel[2] + DIFFERENCE_GREEN)) #and pixel[1] > 200)

def checkForGreen(getImage = 1):
    while(True):
        img = PIL.ImageGrab.grab().load()
        for x in range(TOP_LEFT_X,TOP_RIGHT_X):
            for y in range(TOP_LEFT_Y,TOP_RIGHT_Y):
                if isGreen(img[x,y]):
                    if getImage:
                        return img
                    else:
                        return True
                elif not getImage:
                    return False


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
    return (1- failure/total) > 0.9


def checkForMatch(checkImage):
    for image in images:
        if image != 0:
            if checkForMatchHelper(image,checkImage):
                return images.index(image)
    return False

def pressGivenKey(key):
    print("Pressing " + str(key))
    # human random delay for pressing
    time.sleep(0.35 + random.randrange(1,200)/1000) 
    PressKey(getKeyCode(key))
    # human random delay for length of button press
    time.sleep(0.1 + random.randrange(1,100)/1000)
    ReleaseKey(getKeyCode(key)) 

def getKeyInput(images):
    key = input("Not seen, enter 1-9 to save:")
    try:
        key = int(key)
        if key > 0 and key < 10:
            images[key] = newImage
        else:
            print("invalid input not saving")  
    except:
        print("invalid input not saving")
    
# top left = [58, 1037]
# bottom right = [371,1151]
#top left = 125 1093
#bottom right = 148, 1118
# 52.6 by 29.6
# 132 1106
#print(GetSystemMetrics(0)) #width
#print(GetSystemMetrics(1)) #height

DIFFERENCE_GREEN = 50 
TOP_LEFT_X = 125
TOP_LEFT_Y = 1093
TOP_RIGHT_X = 148
TOP_RIGHT_Y = 1118

if __name__ == '__main__':
    images = [0,0,0,0,0,0,0,0,0]
    while(True):
        newImage = checkForGreen()
        print("Got one")
        check = checkForMatch(newImage)
        if check != False:
            pressGivenKey(check)   
        else:
            getKeyInput(images) 
        while(checkForGreen(0)):
            time.sleep(0.1)
        print("Checking for catch")  
        time.sleep(1)  
