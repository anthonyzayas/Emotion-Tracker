'''
Big thanks to @momogary and @liy9393 for the code which this project was based on
Using microsoft emotion free api. Get an api key here:  https://www.microsoft.com/cognitive-services/en-us/emotion-api
'''
import cv2
import operator
from cv2 import cv
import httplib, urllib, base64

def faceDetection(image):

    #Sets up request from Microsoft API
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXX',
    }

    #Opens webcam.jpg in reading binary form ('rb')
    data = open('webcam.jpg', 'rb').read()
    
    try:
        '''
        Assigns conn to httplib HTTPSConnection method
        which connects to projectoxford api
        '''
        conn = httplib.HTTPSConnection('api.projectoxford.ai')

        '''
        Uses urllib.request method to form a POST request from
        the Microsoft emotion API. Passes webcam.jpg and
        the api key to be processed
        '''
        conn.request("POST", "/emotion/v1.0/recognize" , data , headers)

        '''
        After a request is sent getresponse gets the response from the server.
        Returns an HTTPResponse instance and assigns it to variable response
        '''
        response = conn.getresponse()

        #Reads https response and assigns string to data variable
        data = response.read()

        #Evaluates data so it can be processed by drawBBox function
        data = eval(data) 

        #Closes https connection
        conn.close()

    #Allows for an exception if https connection fails
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return data

#Function to draw box and text around image
def drawBBox(response , image):

    '''
    Example response:
    
    response = [
        {"faceRectangle":{"height":XXX,"left":XXX,"top":XXX,"width":XXX},
         "scores":{"anger":X.XXXE-XX,"contempt":X.XXXXE-XX,"disgust":X.XXXXXE-XX,"fear":X.XXXXE-XX,
         "happiness":X.XXXXXE-XX,"neutral":X.XXXXE-XX,"sadness":X.XXXXE-XX,"surprise":X.XXXXE-XX}},
      
    '''

    #Sets color to RGB value of blue
    color = (255,0,0)

    #Sets font to hershey simplex
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    '''
    sortField here is assigned to
    operator.itemgetter to be used to return a tuple of lookup values.
    '''
    sortField = operator.itemgetter(1)

    #Sets textGap to 15
    textGap = 15

    #Uses OpenCV to assign webcam.jpg to im variable
    im = cv2.imread('webcam.jpg')
    
    for rect in response:
        #Assigns height variable to https response height
        height = rect["faceRectangle"]["height"]
        
        #Assigns width variable to https response width
        width = rect["faceRectangle"]["width"]

        #Assigns start_point to top left coordinate of rectangle in https response
        start_point = (rect["faceRectangle"]["left"],rect["faceRectangle"]["top"])

        #Assigns end_point to bottom right coordinate of rectangle in https response
        end_point = ( start_point[0] + width , start_point[1] + height )

        '''
        Draws a rectangle around picture using OpenCV rectangle method.
        Uses webcam.jpg as its basis, then draws a rectangle using start and end points
        gathered from the https response. Assigns this rectangle color which in RGB values
        is blue. Assigns rectangle a thickness of 2.
        '''
        cv2.rectangle(im, start_point, end_point, color, 2)

        #Sets emotions equal to values in the emotion scores from https response
        emotions = rect["scores"]

        #Iterates through emotions to create a tuple of lookup values
        emotions = sorted(emotions.iteritems(),key=sortField,reverse=True)

        #Loop to sort through tuple of emotion values
        cnt = 1
        for tup in emotions:
            
            #If tuple is less than .1 it is skipped over
            if tup[1] < 0.1:
                continue
            '''
            Else the tuple value for the percentage of the emotion is put
            at the bottom right hand corner of the box in red
            '''
            cv2.putText(im, "%s %.2f" % ( tup[0] ,tup[1]) ,( start_point[0], end_point[1] + textGap * cnt ), font, 0.4,(0,0,255),1)
            cnt += 1

    #Creates a window named face detection
    cv2.namedWindow("face detection")

    #Shows webcam.jpg 
    cv2.imshow("face detection", im)

    #Waits for any key to be pressed to destroy the window created by the drawBBox function
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
#open webcam and capture images   
class Picture():
    
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
            response =  faceDetection(image) 

            #calls drawBBox function which takes the response object and image object to process.
            drawBBox(response , image)
            
