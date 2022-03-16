import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import datetime as dt
import argparse
import comparison_test_base as ctb
# import comparison_test_base as ctb

#root = tk.Tk()
#root.attributes('-fullscreen', True)
global ph
ph = 0

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.attributes('-fullscreen', True)
        self.window.title(window_title)
        self.video_source = video_source
        self.ok=False

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)
      #  self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
     #   self.vid.set(CV2.CAP_PROP_FRAME_HIGHT, 320)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = 520, height = 390)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(window, text="CAPTURE", command=self.snapshot, height=5, width=20)
        self.btn_snapshot.pack(side=tk.LEFT)

        # Predict button
        self.btn_quit=tk.Button(window, text='PREDICT', command=self.predict, height=5, width=20)
        self.btn_quit.pack(side=tk.LEFT)
                
        # Close button
        self.btn_quit=tk.Button(window, text='Close', command=quit, height=5, width=20)
        self.btn_quit.pack(side=tk.LEFT)
        
        self.ph_label = tk.Label(self.window, text=ph, font=('Arial', 70))
        self.ph_label.pack(side=tk.LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay=10
        self.update()

        self.window.mainloop()
        
    def snapshot(self):
        # Get a frame from the video source
        ret,frame=self.vid.get_frame()

        if ret:
            cv2.imwrite("test_strip.jpg" , cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
       
    def update(self):

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if self.ok:
            self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay,self.update)

    def predict(self):
          self.snapshot()
          global ph
          ph = ctb.result()
          self.ph_label.configure(text=ph)
          print("ph : ", ph)
          

class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Command Line Parser
        args=CommandLineParser().args

        
        #create videowriter

        # 1. Video Type
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        self.fourcc=VIDEO_TYPE[args.type[0]]

        # 2. Video Dimension
        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res=STD_DIMENSIONS[args.res[0]]
        print(args.name,self.fourcc,res)
        #self.out = cv2.VideoWriter(args.name[0]+'.'+args.type[0],self.fourcc,10,res)

        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])

        # Get video source width and height
        self.width,self.height=res


    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()

class CommandLineParser:
    
    def __init__(self):

        # Create object of the Argument Parser
        parser=argparse.ArgumentParser(description='Script to record videos')

        # Create a group for requirement 
        # for now no required arguments 
        # required_arguments=parser.add_argument_group('Required command line arguments')

        # Only values is supporting for the tag --type. So nargs will be '1' to get
        parser.add_argument('--type', nargs=1, default=['avi'], type=str, help='Type of the video output: for now we have only AVI & MP4')

        # Only one values are going to accept for the tag --res. So nargs will be '1'
        parser.add_argument('--res', nargs=1, default=['480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument('--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()



def main():
    # Create a window and pass it to the Application object
    App(tk.Tk(),'Video Recorder')
    # ctb.

main()
