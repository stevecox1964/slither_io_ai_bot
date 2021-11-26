import cv2
import numpy as np

from hough_lines import *


def find_nn(point, neighborhood):
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
    nn_idx = nn_idx + j + 1
    return nn, nn_idx 

    


# from
# https://stackoverflow.com/questions/51022381/how-do-i-connect-closest-points-together-using-opencv

def connect_nearest(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, threshold = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    cv2.bitwise_not(threshold, threshold)

    contours, hierarchy  = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    listx = []
    listy=[]

    for i in range(0, len(contours)):
        c = contours[i]
        size = cv2.contourArea(c)
        if size < 1000:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            listx.append(cX)
            listy.append(cY)

    listxy = list(zip(listx,listy))
    listxy = np.array(listxy)

    for i in range(0, len(listxy)):    
            x1 = listxy[i,0]
            y1 = listxy[i,1]
            distance = 0
            secondx = []
            secondy = []
            dist_listappend = []
            sort = []   
            for j in range(0, len(listxy)):      
                if i == j:
                    pass     
                else:
                    x2 = listxy[j,0]
                    y2 = listxy[j,1]
                    distance = np.sqrt((x1-x2)**2 + (y1-y2)**2)
                    secondx.append(x2)
                    secondy.append(y2)
                    dist_listappend.append(distance)

            secondxy = list(zip(dist_listappend,secondx,secondy))
            sort = sorted(secondxy, key=lambda second: second[0])
            sort = np.array(sort)

            cv2.line(img, (x1,y1), (int(sort[0,1]), int(sort[0,2])), (0,0,255), 2)

    return img

def connect_nearest_2(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, threshold = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    cv2.bitwise_not(threshold, threshold)

    contours, hierarchy  = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    listx = []
    listy=[]

    for i in range(0, len(contours)):
        c = contours[i]
        size = cv2.contourArea(c)
        if size < 1000:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            listx.append(cX)
            listy.append(cY)

    listxy = list(zip(listx,listy))
    listxy = np.array(listxy)

    return listxy 


if __name__ == "__main__":

    img = cv2.imread('./img/playing.jpg', cv2.IMREAD_COLOR) 
    #img = connect_nearest(img)
    #cv2.imshow('img', img)


    #taking 6 random points on a board of 200 x 200
    #points = [(10, 10), (115, 42), (36, 98), (78, 154), (167, 141), (189, 4)]

    points = connect_nearest_2(img)

    #reshape
    new_points = []
    for point in points:
        new_points.append(tuple(point))

    points = new_points
    point_count = len(points)
    
    #board = np.ones((580, 512, 3), dtype = np.uint8) * 255
    #board = np.ones((580, 512, 3), dtype = np.uint8) * 255

    for i in range(point_count):
        cv2.circle(img, points[i], 5, (0, 255, 255), -1)

    for j in range(point_count-1):
        nn, nn_idx = find_nn(points[j], points[j+1:])
        points[j+1], points[nn_idx] = points[nn_idx], points[j+1]

    for i in range(point_count-1):
        cv2.arrowedLine(img, points[i], points[i+1], (255, 0, 0), 1, tipLength = 0.07)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    