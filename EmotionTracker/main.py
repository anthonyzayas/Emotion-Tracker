from Tkinter import *
import cv2
import operator
from cv2 import cv
import EmotionTracker
import Tkinter as tk
import tkMessageBox
from collections import deque
from PIL import Image, ImageTk
import tkFileDialog
import time

#Function to create a quit button
def quit_(root):
    root.destroy()
    
#Function that creates a button which saves an image 
def save():
    #Reads the video capture and creates a mat frame named frame
    rval, frame = cam.read()
    #Translates mat frame to jpg
    cv2.imwrite("webcam.jpg", frame);
    #Sets new variable image to webcam.jpg 
    image = "webcam.jpg"

    #Calls faceDetection function which takes the image object to process it. Assigns this https response to response variable
    response = EmotionTracker.faceDetection(image)
                

    #calls drawBBox function which takes the response object and image object to process.
    EmotionTracker.drawBBox(response , image)

#Function to choose existing file
def showWin32Dialog():
    #Defines acceptable filetypes
    filetypes = ["jpg" , "bmp" , "png"]
    #Sets image to an image chosen in tkfiledialog
    image = tkFileDialog.askopenfilename(initialdir = r'C:\Users\v-jingwc\Desktop\\')
    #Allows for jpg, bmp, and png to be processed
    if image.split(".")[-1] in filetypes:
        #Gives a response from chosen photo
        response = EmotionTracker.faceDetection(image)
        EmotionTracker.drawBBox(response , image)
    #If an incorrect file name is given function passes
    elif image == "":
        pass
    #Provides warning in case an inappropriate file type was chosen
    else:
        tkMessageBox.showinfo('Warning','this app just support image of type .jpg/.bmp/.png')
        

def update_image(image_label, cam):
   (readsuccessful, f) = cam.read()
   gray_im = cv2.cvtColor(f, cv2.COLOR_BGR2RGBA)
   a = Image.fromarray(gray_im)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

#Function which calculates fps and returns the fps label
def update_fps(fps_label):
    frame_times = fps_label._frame_times
    frame_times.rotate()
    frame_times[0] = time.time()
    sum_of_deltas = frame_times[0] - frame_times[-1]
    count_of_deltas = len(frame_times) - 1
    try:
       fps = int(float(count_of_deltas) / sum_of_deltas)
    except ZeroDivisionError:
        fps = 0
    fps_label.configure(text='FPS: {}'.format(fps))

#Function which updates the video capture and fps label
def update_all(root, image_label, cam, fps_label):
    update_image(image_label, cam)
    update_fps(fps_label)
    root.after(20, func=lambda: update_all(root, image_label, cam, fps_label))

#Main function which instantiates program
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Emotion Logic") # Title for gui
    image_label = tk.Label(master=root)# label for the video frame
    image_label.pack()
    cam = cv2.VideoCapture(0) #Opens videocapture and sets it to cam
    fps_label = tk.Label(master=root)# label for fps
    fps_label._frame_times = deque([0]*5)  # arbitrary 5 frame average FPS
    fps_label.pack()
    #Button for choosing an existing file
    existing_button = tk.Button(master=root, text='Choose existing file',command=lambda: showWin32Dialog())
    existing_button.pack(side=LEFT, expand = YES, fill = X)
    #Button for taking a picture from webcam
    save_button = tk.Button(master=root, text='Take picture',command=lambda: save())
    save_button.pack(side=LEFT, expand = YES, fill = X)
    # quit button
    quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root))
    quit_button.pack(side=LEFT, expand = YES, fill = X)
    # setup the update callback
    root.after(0, func=lambda: update_all(root, image_label, cam, fps_label))
    root.mainloop()
