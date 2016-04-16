import cv2
import numpy as np

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
Returns 1 if true, 0 if false
"""
def isUp(image): 
    #Creates a mask image
    width, height = frameSize(image)
    blank = blankImage (height/3, width)
    cv2.imshow("1", blank)
    
    #crop and leave the top third
    crop_Up = image[0:height/3, 0:width]
    cv2.imshow("2", crop_Up)
    
    #deterines if the mean number of pixels has increased passed a threshold
    image_count = np.mean(crop_Up)
    blank_count = np.mean(blank)
    #print ("blank is",blank_count)
    #print ("image is ",image_count)
    if (image_count > blank_count) and (image_count - blank_count > 5): 
        print "UP", image_count
        return 1
    
def test():
    a = blankImage(720, 1280)
    isUp(a)
#test()

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
                
        Red_MIN = np.array([0, 0, 200])
        Red_MAX = np.array([100, 100, 255])         
       
        #thresholded color counts. 
        Red_thresh = cv2.inRange(frame, Red_MIN, Red_MAX)
        
        #numpy means of colors.
        meanRed = np.mean(Red_thresh)
        
        #Calculating which color has prominance based on the mean 
        #Also checking if the color is above the threshold we give
        #if (meanRed > 5): 
            #print "Red Detected"
            #print meanRed
        
        isUp(Red_thresh)
            
        # Display the resulting frame
        cv2.imshow('frame', frame)
        cv2.imshow('thresh', Red_thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()        
main()