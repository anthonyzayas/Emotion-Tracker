'''
Big thanks to @momogary and @liy9393 for the code which this project was based on
Using microsoft emotion free api. Get an api key here:  https://www.microsoft.com/cognitive-services/en-us/emotion-api
'''
import cv2
from cv2 import cv
import EmotionTracker
import tkFileDialog
from Tkinter import *
import tkMessageBox
class ConfigWindow(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('Face and Emotion Detection') 
        self.master.geometry('500x300') 
        self.master.resizable(False, False) 
        self.pack(side = TOP,expand = YES,fill = BOTH) 
        bt = Button(self,text='Choose existing file',command=self.showWin32Dialog) 
        bt.pack(side=TOP,expand=NO,fill=Y,pady=20,padx=20)
        bt1 = Button(self,text='Take picture',command=self.takePicture) 
        bt1.pack(side=TOP,expand=NO,fill=Y,pady=20,padx=20)
        
    def showWin32Dialog(self):
        filetypes = ["jpg" , "bmp" , "png"]
        image = tkFileDialog.askopenfilename(initialdir = r'C:\Users\v-jingwc\Desktop\\')
        if image.split(".")[-1] in filetypes:
            response = EmotionTracker.faceDetection(image)
            EmotionTracker.drawBBox(response , image)
        elif image == "":
            pass
        else:
            tkMessageBox.showinfo('Warning','this app just support image of type .jpg/.bmp/.png')

    def takePicture(self):
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

        while rval:
            
            '''
            while rval is true:
            Use opencv method imshow to show the frame in a box called preview
            '''
            cv2.imshow("Press space to take a picture, ESC to exit", frame)
            
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
            ESCKey = 27
            Space = 32
            
            #ASCII value of esc is 27. Pressing it here will exit the program. 
            if key == ESCKey: 
               cv2.destroyAllWindows()
               break

            #ASCII value of space is 32. 
            if key == Space:
                
                #Saves image with OpenCV method SaveImage. Uses Opencv method fromarray on a mat object frame to convert frame to a jpg
                cv.SaveImage("webcam.jpg", cv.fromarray(frame))

                #Sets new variable image to webcam.jpg 
                image = "webcam.jpg"

                #Calls faceDetection function which takes the image object to process it. Assigns this https response to response variable
                response = EmotionTracker.faceDetection(image)
                

                #calls drawBBox function which takes the response object and image object to process.
                EmotionTracker.drawBBox(response , image)

if __name__ == '__main__':
    ConfigWindow().mainloop()
    
