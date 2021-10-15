import numpy as np
import pyautogui
#import imutils
import cv2
import sys
from pynput.mouse import Button, Controller
import time
import random
import math

import datetime


try: 
    import Image
except ImportError:
    from PIL import Image

import pytesseract
# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

import mss
import mss.tools
from PIL import Image
import PIL.ImageOps  
import re
import os
from selenium import webdriver

#Used by mouse class
mouse_controller = Controller()

# These are the dimensions of the window that I'm going to use
window_x = 0
window_y = 100 # The tool bar in chrome is 100 pixels (or so) tall

# Too high resolution and the dataset gets too big.  This is the size of the window to create
width = 600 
height = 600

# size of the game window (the playable area)
window_width = width 
window_height = height - window_y

# coordinates of the center of the game windows
window_center_x = window_width/2
window_center_y = window_y + window_height/2



#######################
# comment these out if you want to consider the whole window
# this is so that you can easily consider less data if you want to
#size_of_window = 200
#window_x = window_center_x - size_of_window/2
#window_y = window_center_y - size_of_window/2
#window_width = size_of_window
#window_height = size_of_window
#######################

# Location of the score that is displayed on the screen
# This will change if you change the dimensions of the window that you create.  
# YOu can easily use mouse.position() to identify the new coordinates
score_x = 88
score_y = 557 
score_width = 91
score_height = 25

play_button_x = 252
play_button_y = 435
play_button_width = 100
play_button_height = 63

# position of the start button on the screen with these window settings
# Note that the shape of the start button changes depending on whether it's a brand new game
# or if you've just died
start_button_position_x = window_center_x
start_button_position_y = 490

# this class is for controlling the mouse using python.  It has a bunch of functions, some of which I don't use here
class Mouse():

    def get_position(self):
        return  mouse_controller.position #point.x, point.y

    def set_position(self,x,y):
        mouse_controller.position = (x,y) #point.x, point.y
        #mouse_controller.move(x,y)
        return
    def move_to(self,x,y) :
        mouse_controller.position = (x,y) #point.x, point.y

    def move_relative(self, x, y):
        mouse_controller.move(x,y)

    def press(self, x, y, button=1):
        mouse_controller.move(x,y)
        mouse_controller.press(Button.left)
        

    def release(self, x, y, button=1):
        mouse_controller.release(Button.left)

    def click(self, button=Button.left):
        x, y = self.position()
        self.press(x, y, button)
        self.release(x, y, button)

    def click_pos(self, x, y, button=Button.left):
        self.move(x, y)
        self.click(button)


# In order to start the game, you have to click on the start button
# if the window is not active, you need two clicks, so this does one click, waits one second, and then clicks again 
# and makes the worm move toward 0
def start_game():
    time.sleep(1)
    mouse.move_to(start_button_position_x, start_button_position_y)
    pyautogui.click()
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    move_to_radians(0)

# this function takes a screenshot of a particular area of the screen
# it also offers the ability to reduce the resolution by selection only every nth pixel...
# there are certainly better ways to reduce the resolution, but this is where I started
# it also lets you decide if you want to convert to grayscale.  
def screenshot(x, y, width, height , reduction_factor = 1 , gray = True ):
    
    sct = mss.mss()
    # The screen part to capture
    scr = {'left': x, 'top': y, 'width': width, 'height': height}

    # Grab the data
    img = sct.grab(scr)
        
    if gray:
        result = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2GRAY)
    else:
        result = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

    img = result[::reduction_factor, ::reduction_factor]

    return img

# this function looks at the right part of the screen for a screenshot of the score 
# then it uses OCR to convert the image of the score into a number
# it will take screenshots until it gets a valid numerical score
# the OCR is not 100% accurate.  The threshold and var values are used to tune the image to maximize the effectiveness of the OCR
def get_score(threshold = 190, var = 10):

    got_it = False
    
    while not got_it:
        
        if is_dead():
            return -1

        img = screenshot(x= score_x, y= score_y, width = score_width, height = score_height, gray = False)

        for rows in range(0, len(img)):
            for cols in range(0, len(img[0])):
                x = img[rows][cols]
                if x[0] > threshold and x[1] > threshold and x[2] > threshold and max(x) - min(x) < var:
                    img[rows][cols] = [0, 0, 0]
                else:
                    img[rows][cols] = [255,255,255]

        #score = pytesseract.image_to_string(img, config='outputbase digits')
        
        #score = re.sub("[^0-9]", "", score)
        
        score = ""
        
        if score != "":            
            score = int(score)
            return score

# This function opens a new browser window, positions and sizes it as desired and then opens slither.io
def open_and_size_browser_window(width, height, x_pos = 0, y_pos = 0, url = 'http://www.slither.io'):

    #opens the browser window
    chrome_options = webdriver.ChromeOptions()    
    chrome_options.add_argument("--disable-infobars")
    driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)

    #sets the size of the window
    driver.set_window_size(width, height)
    
    #repositions the window
    driver.set_window_position(x_pos, y_pos)
    
    #goes to slither.io
    driver.get(url)

    return driver

# this function moves the mouse to a location on a circle with radius = radius
# The user specifies to position on the circle is radians
# This is used for steering the worm
def move_to_radians(radians, radius = 150):
    mouse.move_to(window_center_x + 150 * math.cos(radians),
                  window_center_y + 150 * math.sin(radians))
    return radians

# this function determines the direction that the worm is currently moving based on the mouse's position
def get_direction():
    x, y = mouse.position
    return math.atan2(y, x)

# This function starts a long loop that plays the game.  I have started it out moving randomly
# The challenge is to make the program actually play the game effectively
# The worm often gets a surprising number of points by playing totally randomly
def generate_data(delete_file = False, time_gap = 1, verbose = False):
    print('here in geberate data')
    #initializes the score to 10 -- which is what you start at
    score = 10
    
    # the program will automatically capture data about the screen and the direction, 
    # along with the score 1 second later.
    # there is a flag to control whether or not the file is appended to or overwritten
    if delete_file:
        if os.path.isfile('data.csv'):
            os.remove('data.csv')
    
    #outer loop to control the number of data points gathered
    for i in range(0, 50000):
        print('here in range loop')
        #if dead, reset the score and start a new game
        if is_dead():
            print('You are dead.  Starting the game over.')
            start_game()
            score = 10
            time.sleep(1)            
        else: #randomly change direction
            direction = move_to_radians(random.uniform(0, math.pi*2))
            
        #capture data about what the screen looks like and convert it to a numpy array
        data = screenshot(x=window_x,
                          y=window_y,
                          width=window_width,
                          height=window_height,
                          reduction_factor = 5)
            
        #convert the image array into a vector that can be stored
        values = data.shape[0] * data.shape[1]
        data = data.reshape(values)
        
        #remember what the old score was            
        old_score = score
            
        #wait some time (defaults to 1 second) and then get the new score
        time.sleep(time_gap)
        score = get_score()
            
        #add the image data, the direction, along with the outcome information to a numpy array
        data = np.append(data, [direction, old_score, score, score - old_score])
            
        #write that row out to a file
        with open('data.csv', 'ab') as f:
            np.savetxt(f, [data], fmt='%5d', delimiter=',')

        #print out the results onto the screen if desired
        if verbose:
            print('Data point collected.  Direction: %0.2f. Score changed by: %i' % (direction, score-old_score))

        print('loop')



# instantiate mouse
mouse = Mouse()
