import playsound
import os
import multiprocessing
import time


def playJaws():
    jaws = os.getcwd()+ "\sounds\jaws.mp3"
    playsound.playsound(jaws)


if __name__ == '__main__':
    process = multiprocessing.Process(target=playJaws) # ,args = (1,2) 
    process.start() 
    time.sleep(6)
    process.terminate()
    print("done")
    time.sleep(5)