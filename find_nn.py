import cv2
import numpy as np
import random
import math

from hough_lines import *

#https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors

#Code to calculate the angle between the gun and the target is thus
#myradians = math.atan2(targetY-gunY, targetX-gunX)

#If you want to convert radians to degrees
#mydegrees = math.degrees(myradians)

#To convert from degrees to radians
#myradians = math.radians(mydegrees)



def find_nearest_neighbor(point, neighborhood):
    """
    Finds the nearest neighborhood of a vector.

    Args:
        point (float array): The initial point.
        neighborhood (numpy float matrix): The points that are around the initial point.

    Returns:
        float array: The point that is the nearest neighbor of the initial point.
        integer: Index of the nearest neighbor inside the neighborhood list
    """
    #print(type(point))
    min_dist = float('inf')
    nn = neighborhood[0]
    nn_idx = 0
    for i in range(len(neighborhood)):
        neighbor = neighborhood[i]
        x1 = point[0]
        y1 = point[1]
        x2 = neighbor[0]
        y2 = neighbor[1]
        dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        #dist = cv2.norm(point, neighbor, cv2.NORM_L2)
        if dist < min_dist:
            min_dist = dist
            nn = neighbor
            nn_idx = i

    #nn_idx = nn_idx + j + 1
    #nn_idx = nn_idx + 1
    return nn, nn_idx 

def find_points(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, threshold = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    cv2.bitwise_not(threshold, threshold)

    contours, hierarchy  = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    listx = []
    listy=[]

    for i in range(0, len(contours)):
        c = contours[i]
        size = cv2.contourArea(c)
        if size > 0.0 and size < 1000:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            listx.append(cX)
            listy.append(cY)

    listxy = list(zip(listx,listy))
    points = np.array(listxy)

    #reshape too tuples
    new_points = []
    for point in points:
        new_points.append(tuple(point))

    points = new_points

    return points

def calculate_next_direction(img):
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
    
    #def move_to_radians(radians, radius = 150):
    radians = 0.0 #random.uniform(0, math.pi*2)
    radius = 100
    target_x = center_point_x + radius * math.cos(radians)
    target_y = center_point_y + radius * math.sin(radians)

    target_point = (target_x,target_y)
    
    # Find point nearest to us, really should be in direction we are
    # pointing an a few unit away
    nn_point, nn_idx = find_nearest_neighbor(target_point, points) #[i+1:])

    # Draw circles on points found and our target
    for i in range(point_count-1):
        if i == nn_idx:
            color = (0, 255, 255)
        else:
            color = (255, 0, 0)
        cv2.circle(img, points[i], 5, color, -1)

    #for i in range(point_count-1):
    #    cv2.arrowedLine(img, points[i], points[i+1], (255, 0, 0), 1, tipLength = 0.07) 


    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return -1


#if __name__ == "__main__":

#    img = cv2.imread('./img/playing.jpg', cv2.IMREAD_COLOR)

#    calculate_next_direction(img)

    
    
    