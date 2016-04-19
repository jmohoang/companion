import cv2
import numpy as np

"""
Below are constant variables throughout the program
"""
BOUNDARY_SIZE = 6 #Denominator for the boundary proportion

"""
Takes in an image and returns its height and width
"""
def frameSize(image): 
    width, height = image.shape[:2]
    return (height, width)

"""
Creates a blank black image of the dimensions you give it. 
"""
def blankImage(height, width): 
    image = np.zeros((height,width,3), np.uint8)
    #print np.mean(image) #mean of all black is 0
    return image
"""
Takes in a black and white image. 
Determines whether the upper third of the picture has white. 
Returns 1 if true
"""
def isUp(image): 
    #Creates a bank image the size of the area we want to cover
    width, height = frameSize(image)
    blank = blankImage (height/BOUNDARY_SIZE, width)
    #cv2.imshow("1", blank)
    
    #crop and leave the top third
    crop_Up = image[0:height/BOUNDARY_SIZE, 0:width]
    #cv2.imshow("Up", crop_Up)
    
    #deterines if the mean number of pixels has increased passed a threshold
    image_count = np.mean(crop_Up)
    blank_count = np.mean(blank)
    if (image_count > blank_count) and (image_count - blank_count > 5): 
        #print "UP", image_count
        return 1

"""
Takes in a black and white image. 
Determines whether the lower portion of the picture has white. 
Returns 1 if true
"""
def isDown(image): 
    #Creates a bank image the size of the area we want to cover
    width, height = frameSize(image)
    blank = blankImage (height/BOUNDARY_SIZE, width)    
    
    #Crop and leave the lower portion
    crop_Down = image[height - (height/BOUNDARY_SIZE):height, 0:width]
    #cv2.imshow("Down", crop_Down)
    
    #deterines if the mean number of pixels has increased passed a threshold
    image_count = np.mean(crop_Down)
    blank_count = np.mean(blank)
    if (image_count > blank_count) and (image_count - blank_count > 5): 
        #print "Down", image_count
        return 1    

"""
Takes in a black and white image. 
Determines whether the left portion of the picture has white. 
Returns 1 if true
"""
def isLeft(image): 
    #Creates a bank image the size of the area we want to cover
    width, height = frameSize(image)
    blank = blankImage (height, width/BOUNDARY_SIZE)
    #cv2.imshow("left blank", blank)
    
    #Crop and leave the left portion
    crop_Left = image[0:height, 0:width/BOUNDARY_SIZE]
    #cv2.imshow("Left", crop_Left)
    
    #deterines if the mean number of pixels has increased passed a threshold
    image_count = np.mean(crop_Left)
    blank_count = np.mean(blank)
    if (image_count > blank_count) and (image_count - blank_count > 5): 
        #print "Left", image_count
        return 1    

"""
Takes in a black and white image. 
Determines whether the right portion of the picture has white. 
Returns 1 if true
"""
def isRight(image): 
    #Creates a bank image the size of the area we want to cover
    width, height = frameSize(image)
    blank = blankImage (height, width/BOUNDARY_SIZE)
    #cv2.imshow("right blank", blank)
    
    #Crop and leave the right portion
    crop_Right = image[0:height, width - (width/BOUNDARY_SIZE):width]
    #cv2.imshow("Right", crop_Right)
    
    #deterines if the mean number of pixels has increased passed a threshold
    image_count = np.mean(crop_Right)
    blank_count = np.mean(blank)
    if (image_count > blank_count) and (image_count - blank_count > 5): 
        #print "Right", image_count
        return 1   


"""
Instead of having the main function call out the 4 border-
checking functions, this function checks all of them and calls for corrective 
measures. 
"""
def checkBoundaries(image):
    if isRight(image) == 1: 
        print "Rightoooo" #Instead of this print we would call a corerctive measure function
    if isLeft(image) == 1:
        print "Leftoooo" # Correective measure call
    if isUp(image) == 1: 
        print "Upoooo" # Correective measure call
    if isDown(image): 
        print "Downoo" # Correective measure call

"""
Checks if the object is too close to the camera or too far.
It also calls functions to correct the dictance.
"""
def checkDistance(image): 
    image_count = np.mean(image)
    
    #Too close 
    if image_count > 10: 
        print "Too Close" #corrective function if too close. 
    
    #Too far
    if (image_count > 0.5) and (image_count < 2): 
        print "Too Far"  #corrective function if too far. 
 
"""
For Test Purposes. Ignore!!
"""
def test():
    a = blankImage(720, 1280)
    isRight(a)
#test()

"""
Takes in an image. 
If the picture has colors in teh range specified, 
it returns a black and white picture with white being where the 
color range is. otherwise it returns a blank picture. 
"""
def inColorRange(image): 
    color_min = np.array([45, 100, 100],np.uint8) #110
    color_max = np.array([90, 255, 255],np.uint8) #150    
    thresh = cv2.inRange(image, color_min, color_max)
    return thresh

"""
This function is adapted from homework 3 task 2. 
It currenty checks for the yellow picture. 
"""
def main():
    cap = cv2.VideoCapture(0)
    
    while(True): 
    #for i in range(0, 1):
        # Capture frame-by-frame
        ret, frame = cap.read()        
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
        #thresholded color counts. 
        color_thresh = inColorRange(hsvFrame)
        
        #numpy means of colors.
        meanColor = np.mean(color_thresh)
        
        #Calculating if the color we want is taking prominence 
        #Also checking if the color is above the threshold we give
        #if (meanColor > 3): 
            #print "Color Detected" #This is signal to start following
            #print meanColor
        
        checkBoundaries(color_thresh)
        checkDistance(color_thresh)
            
        # Display the resulting frame
        #cv2.imshow('frame', frame)
        cv2.imshow('thresh', color_thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()        
#main()
