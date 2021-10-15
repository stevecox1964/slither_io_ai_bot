from util_functions import *
from hough_lines import *


# this function determines if the player is dead
# if the player is dead, then the word "Skin" appears where the score would normally be
def is_dead():
    img = screenshot(x= score_x, y= score_y, width = score_width, height = score_height, gray = False)

    # Debug
    winname  = 'is_dead'                   
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 640,30)  # Move it to (40,30)
    cv2.imshow(winname, img)


    #cv2.imshow("OpenCV/Numpy normal", img)
    #print(pytesseract.image_to_string(img))
    if pytesseract.image_to_string(img) == 'Skin':
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
    winname  = 'play again button'                   
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 640,130)  # Move it to (40,30)
    cv2.imshow(winname, img)

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
    winname  = 'play button'                   
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 640,230)  # Move it to (40,30)
    cv2.imshow(winname, img)

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



# open slither.io
driver = open_and_size_browser_window(width = width, height = height)

time.sleep(1)

#Generate data
#generate_data(delete_file = True, verbose = True)

mouse_move_count = 0
mouse_x = -100
mouse_y = 0
is_playing = False

elapst_time = 0

#a = datetime.datetime.now()
#b = datetime.datetime.now()
#delta = b - a
#millis = int(delta.total_seconds() * 1000) # milliseconds

last_time = datetime.datetime.now()

while "Screen capturing":
 
        show_food()

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

            if millis > 2000:
                last_time = datetime.datetime.now()
                direction = move_to_radians(random.uniform(0, math.pi*2))
        
        

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


