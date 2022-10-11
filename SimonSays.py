from os import stat
import RPi.GPIO as GPIO
from time import sleep
import random


#buzzer Defention
buzzer = 13

#led Defention
redLed = 3
greenLed = 5
blueLed = 7
yellowLed = 11

#joystick Defention
button = 12
Portx = 16
Porty = 18

Leds = [redLed, greenLed, blueLed, yellowLed]

#var Defention
delay = 1.5

Moves = []


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(redLed, GPIO.OUT)
    GPIO.setup(greenLed, GPIO.OUT)
    GPIO.setup(blueLed, GPIO.OUT)
    GPIO.setup(yellowLed, GPIO.OUT)

    GPIO.setup(button, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Portx, GPIO.IN)
    GPIO.setup(Porty, GPIO.IN)

    GPIO.setup(buzzer, GPIO.OUT)

def getMoves():
  return Moves
  

def LightOne(LED):
  GPIO.output(redLed, False) 
  GPIO.output(greenLed, False) 
  GPIO.output(blueLed, False) 
  GPIO.output(yellowLed, False) 

  GPIO.output(LED, True) 

def LightAll():
  GPIO.output(redLed, True) 
  GPIO.output(greenLed, True) 
  GPIO.output(blueLed, True) 
  GPIO.output(yellowLed, True) 

def LightNone():
  GPIO.output(redLed, False) 
  GPIO.output(greenLed, False) 
  GPIO.output(blueLed, False) 
  GPIO.output(yellowLed, False) 

def ShowMovesNeeded(failed):
    
    if failed:
      getMoves().clear()

    getMoves().append(Leds[random.randint(0,3)])

    for Led in getMoves():
        LightOne(Led)
        GPIO.output(buzzer, True) 
        sleep(0.2)
        GPIO.output(buzzer, False) 
        sleep(delay)
    print(getMoves())    
    playGame()    

def GetJoystickPos():

     
  Px = GPIO.input(Portx)
  Py = GPIO.input(Porty)

  if Px == 1 and Py == 1:
    return yellowLed
  elif Px == 0 and Py == 1:
    return redLed
  elif Px == 1 and Py == 0:
    return blueLed
  else:
    return greenLed

def UpdatePositionOfJoy():
  Px = GPIO.input(Portx)
  Py = GPIO.input(Porty)

  if Px == 1 and Py == 1:
    LightOne(yellowLed)
  elif Px == 0 and Py == 1:
    LightOne(redLed)
  elif Px == 1 and Py == 0:
    LightOne(blueLed)
  else:
    LightOne(greenLed)



def playGame():
  
  pos = 0
  while True:
    UpdatePositionOfJoy()
    if pos == len(getMoves()):
      print("won", "pos = ", pos, "length = ", len(getMoves()))
      ShowMovesNeeded(False)
      break
    elif GPIO.input(button) == 0 and getMoves()[pos] != GetJoystickPos():
      print("lost round Moves:", getMoves()[pos], "input:", GetJoystickPos(),"pos",pos)

      LightAll()
      GPIO.output(buzzer, True) 
      sleep(1.5)
      LightNone()
      GPIO.output(buzzer, False) 

      pos = 0
      ShowMovesNeeded(True)
      break
    elif GPIO.input(button) == 0 and getMoves()[pos] == GetJoystickPos():
      print("add")
      pos += 1
      GPIO.output(buzzer, True) 
      sleep(0.2)
      GPIO.output(buzzer, False) 

      




setup()
ShowMovesNeeded(False)
LightNone()
GPIO.cleanup()