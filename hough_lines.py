import cv2
import numpy as np

def connect():

    img = cv2.imread('./img/points.jpg', cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, threshold = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    cv2.bitwise_not(threshold, threshold)

    #im, contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
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

    cv2.imshow('img', img)
        #cv2.imwrite('connected.png', img)

def process_canny(img):

    kernel = np.ones((1,1), np.uint8)
    color = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, np.array([151, 96, 175]), np.array([154, 255, 255]))
    color[mask>0]=(255,255,152)

    lines = cv2.Canny(color, threshold1=271, threshold2=398)
    img_dilation = cv2.dilate(lines, kernel, iterations=1) 

    return img_dilation
    


def draw_image(img, x1, x2 , y):

    kernel = np.ones((2,2), np.uint8)
    color = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, np.array([151, 96, 175]), np.array([154, 255, 255]))
    color[mask>0]=(255,255,152)

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lines = cv2.Canny(color, threshold1=271, threshold2=398)
    img_dilation = cv2.dilate(lines, kernel, iterations=1) 

    cv2.imshow(f"Dilation", img_dilation)
    cv2.waitKey(0)

    '''

    HoughLines = cv2.HoughLinesP(img_dilation, 1, np.pi/180, 37, 3, 22)
    if HoughLines is not None:
        for line in HoughLines:
            coords = line[0]
            cv2.line(color, (coords[0], coords[1]), (coords[2], coords[3]), [0,255,255], 3)

    cv2.imshow(f"HoughLines", color)
    cv2.waitKey(0)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=17, minRadius=10, maxRadius=14)

    if circles is not None:
        circles = np.uint16(circles)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(color, (x,y), r, (0, 0, 255), 5)
    else:
        print("No Circles")

    color = cv2.circle(color, (x1,y), radius=2, color=(0, 0, 0), thickness=-1)
    color = cv2.circle(color, (x2,y), radius=2, color=(0, 0, 255), thickness=1)

    # Debug
    #winname  = 'food window'                   
    #cv2.namedWindow(winname)        # Create a named window
    #cv2.moveWindow(winname, 640,630)  # Move it to (40,30)
    #cv2.imshow(winname, color)

    cv2.imshow(f"Circles", color)
    cv2.waitKey(0)
    '''

if __name__ == "__main__": 

    #img = cv2.imread('./img/playing.jpg', cv2.IMREAD_COLOR)
    #draw_image(img, 218, 240, 23)
    #img_dilation = process_canny(img)

    #cv2.imshow(f"Dilation", img_dilation)

    connect()

    
    cv2.waitKey(0)