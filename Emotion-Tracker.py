'''
Big thanks to @momogary and @liy9393 for the code which this project was based on
Using microsoft emotion free api. Get an api key here:  https://www.microsoft.com/cognitive-services/en-us/emotion-api
'''
import cv2
from cv2 import cv
from Tkinter import *
import tkMessageBox
import httplib, urllib, base64
import tkFileDialog
def faceDetection(image):
    
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXX',
    }

    '''
    params = urllib.urlencode({
    'url': 'http://i.epochtimes.com/assets/uploads/2011/03/110312195005100445.jpg',
    })
    '''

    data = open('webcam.jpg', 'rb').read()
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')

        conn.request("POST", "/emotion/v1.0/recognize" , data , headers)

        response = conn.getresponse()

        data = response.read()
        #print(data)
        data = eval(data)  # type list
        #print type(data)
        #print data
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return data

def drawBBox(response , image):
    #from PIL import Image
    '''
    response = [
        {"faceRectangle":{"height":113,"left":624,"top":109,"width":113},"scores":{"anger":3.094097E-06,"contempt":5.47389654E-08,"disgust":1.40311486E-05,"fear":2.1335E-09,"happiness":0.9999826,"neutral":1.21930185E-07,"sadness":2.03058121E-08,"surprise":7.509437E-08}},
        {"faceRectangle":{"height":112,"left":230,"top":145,"width":112},"scores":{"anger":1.62075583E-12,"contempt":8.48001E-13,"disgust":4.43286114E-13,"fear":1.20183927E-15,"happiness":1.0,"neutral":5.69783977E-12,"sadness":2.131319E-14,"surprise":3.8522345E-12}},
        {"faceRectangle":{"height":103,"left":525,"top":184,"width":103},"scores":{"anger":5.1391353E-11,"contempt":1.26054183E-13,"disgust":6.300444E-11,"fear":2.00125181E-12,"happiness":1.0,"neutral":1.11211517E-12,"sadness":5.692164E-14,"surprise":6.25029639E-10}},
        {"faceRectangle":{"height":100,"left":348,"top":186,"width":100},"scores":{"anger":1.46614942E-10,"contempt":6.196312E-10,"disgust":3.89794273E-11,"fear":1.38707434E-10,"happiness":1.0,"neutral":4.158724E-09,"sadness":5.360124E-12,"surprise":1.9608418E-08}},
        {"faceRectangle":{"height":98,"left":121,"top":205,"width":98},"scores":{"anger":8.750456E-07,"contempt":1.87719866E-06,"disgust":6.564448E-07,"fear":4.57608245E-08,"happiness":0.999996245,"neutral":2.52363776E-07,"sadness":3.497753E-08,"surprise":3.27670975E-08}}
    ]
    '''

    import cv2
    import operator

    color = (255,0,0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    sortField = operator.itemgetter(1)
    textGap = 15

    im = cv2.imread('webcam.jpg')
    for rect in response:
        height = rect["faceRectangle"]["height"]
        width = rect["faceRectangle"]["width"]
        start_point = (rect["faceRectangle"]["left"],rect["faceRectangle"]["top"])
        end_point = ( start_point[0] + width , start_point[1] + height )
        cv2.rectangle(im, start_point, end_point, color, 2)

        emotions = rect["scores"]
        emotions = sorted(emotions.iteritems(),key=sortField,reverse=True)

        cnt = 1
        for tup in emotions:
            if tup[1] < 0.1:
                continue
            cv2.putText(im, "%s %.2f" % ( tup[0] ,tup[1]) ,( start_point[0], end_point[1] + textGap * cnt ), font, 0.4,(0,0,255),1)
            cnt += 1

    cv2.namedWindow("face detection")
    cv2.imshow("face detection", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
#open webcam and capture images   
class Picture():
    
    #creates a window named preview in windows
    cv2.namedWindow("preview")
    
    #Creates a variable called vc which holds the Video capture of the first detected device. This is noted by the (0).
    vc = cv2.VideoCapture(0)
    
    """
    try to get the first frame
    if video capture is opened rval is set to true and a new mat variable named frame is set to
    vc.read
    """
    
    if vc.isOpened(): 
        rval, frame = vc.read()
    else:
        rval = False
    
    print "\n\n\n\n\nPress space to take picture; press ESC to exit"

   
    while rval:
        
        """
        while rval is true:
        Use opencv method imshow to show the frame in a box called preview
        """
        cv2.imshow("preview", frame)
        
        #reads frame by frame through the video capture while a webcam is open
        rval, frame = vc.read()
        
        """
        Writing waitKey(40) will make the program wait for 40 millisecond.
        In this duration it will also check whether any key is pressed or not .
        If any key is pressed than this will return the ASCII value of that pressed key. 
        As explained in the OpenCV documentation, HighGui (imshow() is a function of HighGui)
        needs a call of waitKey regularly, in order to process its event loop.
        """
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
            
