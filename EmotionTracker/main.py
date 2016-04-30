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

def quit_(root):
    root.destroy()

def save():
    rval, frame = cam.read()
    cv2.imwrite("webcam.jpg", frame);
    #Sets new variable image to webcam.jpg 
    image = "webcam.jpg"

    #Calls faceDetection function which takes the image object to process it. Assigns this https response to response variable
    response = EmotionTracker.faceDetection(image)
                

    #calls drawBBox function which takes the response object and image object to process.
    EmotionTracker.drawBBox(response , image)

def showWin32Dialog():
    filetypes = ["jpg" , "bmp" , "png"]
    image = tkFileDialog.askopenfilename(initialdir = r'C:\Users\v-jingwc\Desktop\\')
    if image.split(".")[-1] in filetypes:
        response = EmotionTracker.faceDetection(image)
        EmotionTracker.drawBBox(response , image)
    elif image == "":
        pass
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


def update_all(root, image_label, cam, fps_label):
    update_image(image_label, cam)
    update_fps(fps_label)
    root.after(20, func=lambda: update_all(root, image_label, cam, fps_label))


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Emotion Detection")
    image_label = tk.Label(master=root)# label for the video frame
    image_label.pack()
    cam = cv2.VideoCapture(0)
    fps_label = tk.Label(master=root)# label for fps
    fps_label._frame_times = deque([0]*5)  # arbitrary 5 frame average FPS
    fps_label.pack()
    existing_button = tk.Button(master=root, text='Choose existing file',command=lambda: showWin32Dialog())
    existing_button.pack(side=LEFT, expand = YES, fill = X)
    save_button = tk.Button(master=root, text='Take picture',command=lambda: save())
    save_button.pack(side=LEFT, expand = YES, fill = X)
    # quit button
    quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root))
    quit_button.pack(side=LEFT, expand = YES, fill = X)
    # setup the update callback
    root.after(0, func=lambda: update_all(root, image_label, cam, fps_label))
    root.mainloop()
