from pynput import mouse
import numpy as np
import cv2
import pyautogui
import sys

# Create point matrix get coordinates of mouse click on image
point_matrix = np.zeros((2,2),np.int16)

counter = -1

def on_move(x, y):
    pass
    # print('Pointer moved to {0}'.format(
    #     (x, y)))

def on_click(x, y, button, pressed):
    global counter
    if pressed:
        # print('{0} {1} at {2}'.format(counter,
        #     'Pressed' if pressed else 'Released',
        #     (x, y))) 
        point_matrix[counter] = x,y
        counter += 1
        
    if counter == 2 :
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    pass
    # print('Scrolled {0} at {1}'.format(
    #     'down' if dy < 0 else 'up',
    #     (x, y)))

# Collect events until released
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()

starting_x = point_matrix[0][0]
starting_y = point_matrix[0][1]
 
ending_x = point_matrix[1][0]
ending_y = point_matrix[1][1]    
print(starting_x)
print(starting_y)
print(ending_x)
print(ending_y)

# take screenshot using pyautogui
# image = pyautogui.screenshot()
image = pyautogui.screenshot(region=(starting_x, starting_y, ending_x-starting_x, ending_y-starting_y))

# since the pyautogui takes as a 
# PIL(pillow) and in RGB we need to 
# convert it to numpy array and BGR 
# so we can write it to the disk
image = cv2.cvtColor(np.array(image),
                            cv2.COLOR_RGB2BGR)
        
# writing it to the disk using opencv
cv2.imwrite(sys.argv[1], image)

