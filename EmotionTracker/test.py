from Tkinter import *
import cv2
import operator
from cv2 import cv
import httplib, urllib, base64

'''
Root = Tk() is the main loop where gui stuff needs to go under
'''

root = Tk() #Makes the window
root.wm_title("Emotion Detector") #Makes the title that will appear in the top left
root.config(background = "#FFFFFF")
'''
this below code works a camera by itself
'''

##def camera():
##    cv2.namedWindow("Emotion Tracker")
##    vc = cv2.VideoCapture(0)
##
##    if vc.isOpened(): # try to get the first frame
##        rval, root = vc.read()
##    else:
##        rval = False
##
##    while rval:
##        cv2.imshow("preview", circleCanvas)
##        rval, root = vc.read()
##        key = cv2.waitKey(20)
##        if key == 27: # exit on ESC
##            break

'''this part will run code in camera in a gui by istelf
'''

##
##def quit_(root):
##    root.destroy()
##
##def update_image(image_label, cam):
##    (readsuccessful, f) = cam.read()
##    gray_im = cv2.cvtColor(f, cv2.COLOR_BGR2RGBA)
##    a = Image.fromarray(gray_im)
##    b = ImageTk.PhotoImage(image=a)
##    image_label.configure(image=b)
##    image_label._image_cache = b  # avoid garbage collection
##    root.update()
##
##
##def update_fps(fps_label):
##    frame_times = fps_label._frame_times
##    frame_times.rotate()
##    frame_times[0] = time.time()
##    sum_of_deltas = frame_times[0] - frame_times[-1]
##    count_of_deltas = len(frame_times) - 1
##    try:
##        fps = int(float(count_of_deltas) / sum_of_deltas)
##    except ZeroDivisionError:
##        fps = 0
##    fps_label.configure(text='FPS: {}'.format(fps))
##
##
##def update_all(root, image_label, cam, fps_label):
##    update_image(image_label, cam)
##    update_fps(fps_label)
##    root.after(20, func=lambda: update_all(root, image_label, cam, fps_label))

##
##if __name__ == '__main__':
##    root = tk.Tk() 
##    image_label = tk.Label(master=root)# label for the video frame
##    image_label.pack()
##    cam = cv2.VideoCapture(1) 
##    fps_label = tk.Label(master=root)# label for fps
##    fps_label._frame_times = deque([0]*5)  # arbitrary 5 frame average FPS
##    fps_label.pack()
##    # quit button
##    quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root))
##    quit_button.pack()
##    # setup the update callback
##    root.after(0, func=lambda: update_all(root, image_label, cam, fps_label))
##    root.mainloop()



'''
This code is a Gui by itself
'''

def redCircle():
    circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='red')
    colorLog.insert(0.0, "Red\n")

def yelCircle():
    circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='yellow')
    colorLog.insert(0.0, "Yellow\n")

def grnCircle():
    circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='green')
    colorLog.insert(0.0, "Green\n")


#Left Frame and its contents
leftFrame = Frame(root, width=200, height = 600)
leftFrame.grid(row=0, column=0, padx=10, pady=2)

Label(leftFrame, text="Instructions:").grid(row=0, column=0, padx=10, pady=2)

Instruct = Label(leftFrame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
Instruct.grid(row=1, column=0, padx=10, pady=2)

try:
    imageEx = PhotoImage(file = 'image.gif')
    Label(leftFrame, image=imageEx).grid(row=2, column=0, padx=10, pady=2)
except:
    print("Image not found")

#Right Frame and its contents
rightFrame = Frame(root, width=200, height = 600 )
rightFrame.grid(row=0, column=1, padx=10, pady=2)

circleCanvas = Canvas(rightFrame, width=100, height=100)
circleCanvas.grid(row=0, column=0, padx=10, pady=2)

btnFrame = Frame(rightFrame, width=200, height = 200)
btnFrame.grid(row=1, column=0, padx=10, pady=2)

colorLog = Text(rightFrame, width = 30, height = 10, takefocus=0)
colorLog.grid(row=2, column=0, padx=10, pady=2)

redBtn = Button(btnFrame, text="Red", command=redCircle)
redBtn.grid(row=0, column=0, padx=10, pady=2)

yellowBtn = Button(btnFrame, text="Yellow", command=yelCircle)
yellowBtn.grid(row=0, column=1, padx=10, pady=2)

greenBtn = Button(btnFrame, text="Green", command=grnCircle)
greenBtn.grid(row=0, column=2, padx=10, pady=2)


root.mainloop() #start monitoring and updating the GUI
