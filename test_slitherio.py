from util_functions import *
from hough_lines import *
from find_nn import *


# this function determines if the player is dead
# if the player is dead, then the word "Skin" appears where the score would normally be
def get_score():
    img = screenshot(x= score_x+5, 
                     y= score_y-5, 
                     width = 25, 
                     height = 15, 
                     gray = True)

    # Debug
    winname  = 'score'                   
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 640,30)  # Move it to (40,30)
    cv2.imshow(winname, img)

    image_text = pytesseract.image_to_string(img)

    print(image_text)



# this function determines if the player is dead
# if the player is dead, then the word "Skin" appears where the score would normally be
def is_dead():
    img = screenshot(x= score_x, 
                     y= score_y, 
                     width = score_width, 
                     height = score_height, 
                     gray = False)

    # Debug
    #winname  = 'is_dead'                   
    #cv2.namedWindow(winname)        # Create a named window
    #cv2.moveWindow(winname, 640,30)  # Move it to (40,30)
    #cv2.imshow(winname, img)


    #cv2.imshow("OpenCV/Numpy normal", img)
    #print(pytesseract.image_to_string(img))

    image_text = pytesseract.image_to_string(img)

    #print(image_text)

    if image_text == 'Skin':
        return True
    else: 
        return False


#-------------------------------------------------------------------------------------------------------------------
# if the player is dead, and we need to click play again the word "Play Again" appears where the score would normally be
def is_play_again():

    results = False

    img = screenshot(x= play_button_x, 
                     y= play_button_y, 
                     width = play_button_width, 
                     height = play_button_height, 
                     gray = False)

    # Debug
    #winname  = 'play again button'                   
    #cv2.namedWindow(winname)        # Create a named window
    #cv2.moveWindow(winname, 640,130)  # Move it to (40,30)
    #cv2.imshow(winname, img)

    results = pytesseract.image_to_string(img)#.strip()
    #print(results)
    
    if len(results) > 0:
        if 'Plivhaain' in results:
            results = True #'Play Again'
    
    return results

#-------------------------------------------------------------------------------------------------------------------
# if the player is dead, and we need to click play again the word "Play Again" appears where the score would normally be
def is_play():

    results = ''
    img = screenshot(x= 280, 
                     y= 463, 
                     width = play_button_width, 
                     height = play_button_height, 
                     gray = False)

    # Debug
    #winname  = 'play button'                   
    #cv2.namedWindow(winname)        # Create a named window
    #cv2.moveWindow(winname, 640,230)  # Move it to (40,30)
    #cv2.imshow(winname, img)

    results = pytesseract.image_to_string(img)#.strip()

    print(results)
    
    if len(results) > 0:
        if 'Playloﬂl' in results:
            results = 'Play'
            
    return results
#-------------------------------------------------------------------------------------------------------------------
# 
def show_food():


    img = screenshot(x= window_x, 
                     y= window_y, 
                     width = window_width, 
                     height = window_height, 
                     gray = False)

    img = process_canny(img)

    # Debug
    winname  = 'food'                   
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 640,430)  # Move it to (40,30)
    cv2.imshow(winname, img)

    return

#-------------------------------------------------------------------------------------------------------------------
# 
def find_food(last_direction):

    img = screenshot(x= window_x, 
                     y= window_y, 
                     width = window_width, 
                     height = window_height, 
                     gray = False)

    # Get shape if image
    height, width, channels = img.shape
    #print(height, width, channels)

    # create our center xy coords
    center_point_x = width/2
    center_point_y = height/2

    #print(center_point_x,center_point_y)

    # Take image and converts to hough/black and white and
    # and gets contur points
    points = find_points(img)

    point_count = len(points)

    if point_count < 3:
        return None
    
    #radians = 0.0 #random.uniform(0, math.pi*2)
    radius = 75
    target_x = center_point_x + radius * math.cos(last_direction)
    target_y = center_point_y + radius * math.sin(last_direction)

    target_point = (target_x,target_y)

    # Find point nearest to us, really should be in direction we are
    # pointing an a few unit away
    nn_point, nn_idx = find_nearest_neighbor(target_point, points) #[i+1:])

    x1 = center_point_x
    y1 = center_point_y
    x2 = nn_point[0]
    y2 = nn_point[1]

    target_dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)

    print(target_dist)

    # Draw circles on points found and our target
    for i in range(point_count-1):
        if i == nn_idx:
            color = (0, 255, 255)
        else:
            cur_point = points[i]
            x1 = center_point_x
            y1 = center_point_y
            x2 = cur_point[0]
            y2 = cur_point[1]

            dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
            
            color = (np.clip(dist,0,255), 0, 0)

        cv2.circle(img, points[i], 5, color, -1)

    # Debug
    winname  = 'food'                   
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 640,430)  # Move it to (40,30)
    cv2.imshow(winname, img)

    if target_dist > 20 and target_dist < 220:
        new_direction = math.atan2(nn_point[1]-center_point_y, nn_point[0]-center_point_x)
    else:
        print('RANDO')
        new_direction = random.uniform(0, math.pi*2) 

    return new_direction

#-------------------------------------------------------------------------------------------------------------------
# this function moves the mouse to a location on a circle with radius = radius
# The user specifies to position on the circle is radians
# This is used for steering the worm
def move_to_radians(radians, radius = 150):
    mouse.move_to(window_center_x + radius * math.cos(radians),
                  window_center_y + radius * math.sin(radians))
    return radians


# open slither.io
driver = open_and_size_browser_window(width = width, height = height)

time.sleep(1)


mouse_move_count = 0
mouse_x = -100
mouse_y = 0
is_playing = False

elapst_time = 0


last_time = datetime.datetime.now()
last_direction = 0.0

while True:

        #get_score()

        we_dead = is_dead()
        play_again = is_play_again()

        if we_dead and play_again:
            #start_game()
            time.sleep(2)
            mouse.move_to(255,463)
            pyautogui.click()
            time.sleep(1)
            is_playing = True
            
        if is_playing:

            next_time = datetime.datetime.now()
            delta = next_time - last_time
            millis = int(delta.total_seconds() * 1000) # milliseconds

            if millis > 1000:

                #myradians = math.atan2(targetY-gunY, targetX-gunX)

                new_direction = find_food(last_direction)
                if new_direction == None:
                    print('No food')
                    new_direction = random.uniform(0, math.pi*2)
                
                last_time = datetime.datetime.now()
                last_direction = move_to_radians(new_direction) #random.uniform(0, math.pi*2))
                #last_direction
        
        

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


