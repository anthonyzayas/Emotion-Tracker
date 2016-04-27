'''
Big thanks to @momogary and @liy9393 for the code which this project was based on
Using microsoft emotion free api. Get an api key here:  https://www.microsoft.com/cognitive-services/en-us/emotion-api
'''
import cv2
import operator
from cv2 import cv
import httplib, urllib, base64
import EmotionTracker 
def main():
    
    #creates a window named preview in windows
    cv2.namedWindow("preview")
    
    #Creates a variable called vc which holds the Video capture of the first detected device. This is noted by the (0).
    vc = cv2.VideoCapture(0)
    
    '''
    try to get the first frame
    if video capture is opened rval is set to true and a new mat variable named frame is set to
    vc.read
    '''
    
    if vc.isOpened(): 
        rval, frame = vc.read()
    else:
        rval = False
    
    print "\n\n\n\n\nPress space to take picture; press ESC to exit"

   
    while rval:
        
        '''
        while rval is true:
        Use opencv method imshow to show the frame in a box called preview
        '''
        cv2.imshow("preview", frame)
        
        #reads frame by frame through the video capture while a webcam is open
        rval, frame = vc.read()
        
        '''
        Writing waitKey(40) will make the program wait for 40 millisecond.
        In this duration it will also check whether any key is pressed or not .
        If any key is pressed than this will return the ASCII value of that pressed key. 
        As explained in the OpenCV documentation, HighGui (imshow() is a function of HighGui)
        needs a call of waitKey regularly, in order to process its event loop.
        '''
        key = cv2.waitKey(40)
        
        #ASCII value of esc is 27. Pressing it here will exit the program. 
        if key == 27: 
            break

        #ASCII value of space is 32. 
        if key == 32:
            
            #Saves image with OpenCV method SaveImage. Uses Opencv method fromarray on a mat object frame to convert frame to a jpg
            cv.SaveImage("webcam.jpg", cv.fromarray(frame))

            #Sets new variable image to webcam.jpg through OpenCV
            image = cv.LoadImage("webcam.jpg")

            #Calls faceDetection function which takes the image object to process it. Assigns this https response to response variable
            response = EmotionTracker.faceDetection(image)
            

            #calls drawBBox function which takes the response object and image object to process.
            EmotionTracker.drawBBox(response , image)

if __name__ == "__main__":
    main()
