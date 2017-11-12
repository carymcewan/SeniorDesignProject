from StepperClient import StepperClient
from emailClient import EmailClient
from s3Upload import S3Client
from picamera import PiCamera
from newlibply import *
from scipy import ndimage
import time

import tkinter.ttk as ttk
from tkinter import *

# Declare variables
totalSteps = 400

captureFrequency = 1
stepCount = 0
stepDelay = 25

processImageCount = 0

# Initialize modules
camera = PiCamera()
camera.shutter_speed = 1250

emailClient = EmailClient("Group B Creol", "seniordesigngroupb@gmail.com", "GroupBCreol")
s3Client = S3Client()
stepperClient = StepperClient("right")

class Scanner():
    def __init__(self, root):
        self.proceed = None
        self.root = root
        self.root.geometry("300x225")

        self.status = StringVar()
        self.status.set("Preparing to scan...")
        statusLabel = Label(self.root, textvariable=self.status, bd=1, relief=SUNKEN, anchor=W)
        statusLabel.pack(fill=X, side=BOTTOM)

        topFrame = Frame(self.root)
        topFrame.pack(side=TOP)

        bottomFrame = Frame(self.root)
        bottomFrame.pack(side=BOTTOM)

        middleFrame = Frame(self.root)
        middleFrame.pack(side=BOTTOM)

        self.startButton = Button(middleFrame, text="Start", command=self.start)
        self.startButton.grid(row=0, column=0, padx=10, pady=10)

        self.pauseButton = Button(middleFrame, text="Pause", command=self.pause)
        self.pauseButton.grid(row=0, column=1, padx=10, pady=10)
        self.pauseButton["state"] = "disabled"

        self.resetButton = Button(middleFrame, text="Reset", command=self.reset)
        self.resetButton.grid(row=0, column=2, padx=10, pady=10)
        self.resetButton["state"] = "disabled"

        self.progress = DoubleVar()
        self.progress.set(stepCount)
        self.progressbar = ttk.Progressbar(bottomFrame, variable=self.progress, maximum=totalSteps)

        fileNameLabel = Label(topFrame, text="File", pady=5)
        nameLabel = Label(topFrame, text="Name", pady=5)
        emailLabel = Label(topFrame, text="Email", pady=5)
        self.fileName = StringVar()
        self.name = StringVar()
        self.email = StringVar()
        self.fileNameEntry = Entry(topFrame, textvariable=self.fileName, state=DISABLED)
        self.nameEntry = Entry(topFrame, textvariable=self.name, state=DISABLED)
        self.emailEntry = Entry(topFrame, textvariable=self.email, state=DISABLED)

        fileNameLabel.grid(row=0)
        nameLabel.grid(row=1)
        emailLabel.grid(row=2)

        self.fileNameEntry.grid(row=0, column=1, pady=5)
        self.nameEntry.grid(row=1, column=1, pady=5)
        self.emailEntry.grid(row=2, column=1, pady=5)

        self.sendEmailButton = Button(topFrame, text="Send Email", command=self.sendEmail, state=DISABLED)
        self.sendEmailButton.grid(row=3, columnspan=2, pady=10)

        self.root.mainloop()

    def start(self):
        self.resetButton["state"] = "normal"
        self.pauseButton["state"] = "normal"
        self.progressbar.pack(fill=X, expand=1, pady=5)
        self.root.update_idletasks()
        self.scan()  # start repeated checking

    def pause(self):
        global proceed
        global stepCount
        if proceed:
            self.root.after_cancel(proceed)
            proceed = None
        self.status.set("Scanning... {}% Paused".format(int((stepCount / totalSteps) * 100)))

    def reset(self):
        global proceed
        global stepCount
        if proceed:
            self.root.after_cancel(proceed)
            proceed = None
        stepCount = 0
        self.progress.set(stepCount)
        self.fileNameEntry["state"] = "disabled"
        self.nameEntry["state"] = "disabled"
        self.emailEntry["state"] = "disabled"
        self.sendEmailButton["state"] = "disabled"
        self.status.set("Scanning... {}% Reset".format(int((stepCount / totalSteps) * 100)))

    def scan(self):
        global stepCount
        global proceed
        if stepCount < totalSteps:
            stepperClient.step()
            stepCount += 1
            self.status.set("Scanning... {}%".format(int((stepCount / totalSteps) * 100)))
            self.progress.set(stepCount)
            if stepCount % captureFrequency == 0:
                imageNumber = int(stepCount / captureFrequency)
                camera.capture('images/image{}.jpg'.format(imageNumber))
            proceed = self.root.after(stepDelay, self.scan)  # check again in 1 second
        else:
            self.status.set("Scanning... Complete")
            self.root.after(1000, self.status.set, "Preparing to construct 3-D representation...")
            self.root.after(1000, self.processImages, 0, 0)

    def processImages(self, imageCount, vertexCount, fileName="image", ):
        path = "imagesCylinder/"

        if imageCount == 0:
            self.resetButton["state"] = "disabled"
            self.pauseButton["state"] = "disabled"
            self.startButton["state"] = "disabled"
            self.status.set("Constructing 3-D representation... 0%")

            init_ply()

        if imageCount < totalSteps:
            imageCount += 1
            self.status.set("Constructing 3-D representation... {}%".format(int((imageCount / totalSteps) * 100)))
            self.progress.set(imageCount)
            self.root.update_idletasks()
            theta = imageCount * (np.pi / 200)
            nim = ndimage.imread(path + fileName + str(imageCount) + ".jpg")
            pcl = point_detection(nim)
            diff = np.zeros((3, pcl.shape[1]))
            diff[0].fill(1751)
            pcl -= diff
            rot = pcl_rotate(theta, pcl)

            if rot.size != 0:
                append_ply(rot)
            vertexCount += pcl.shape[0]

            proceed = self.root.after(0, self.processImages, imageCount, vertexCount)

        else:
            update_vertex_count_ply(vertexCount)
            self.status.set("Constructing 3-D representation... Complete")
            self.root.after(1000, self.status.set, "3-D file now ready for upload.")
            self.fileNameEntry["state"] = "normal"
            self.nameEntry["state"] = "normal"
            self.emailEntry["state"] = "normal"
            self.sendEmailButton["state"] = "normal"


    def sendEmail(self):
        self.status.set("Uploading file to S3...")
        self.root.update_idletasks()
        link = s3Client.uploadFile("matply.ply", "groupbcreol", self.fileName.get() + ".jpg")
        self.status.set("Uploading file to S3... Complete")
        self.root.update_idletasks()
        self.status.set("Sending email...")
        self.root.update_idletasks()
        emailClient.sendScanEmail(self.name.get(), self.email.get(), link)
        self.status.set("Sending email... Complete")

root = Tk(className="3d Scanning System")
scanner = Scanner(root)