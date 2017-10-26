from StepperClient import StepperClient
from emailClient import EmailClient
from s3Upload import S3Client
from picamera import PiCamera
from time import sleep

import tkinter.ttk as ttk
from tkinter import *

# Declare variables
steps = 400
delay = 0.05
captureFrequency = 1
stepCount = 0

# Initialize modules
camera = PiCamera()
camera.resolution = (2592, 1944)
# camera.start_preview() # Comment out for now to bypass camera preview
emailClient = EmailClient("Group B Creol", "seniordesigngroupb@gmail.com", "GroupBCreol")
s3Client = S3Client()
# stepperClient = StepperClient("right")

def scan():
    for step in range(0, steps):
        # stepperClient.step()
        if step % captureFrequency == 0:
            imageNumber = int(step / captureFrequency)
            camera.capture('images/image{}.jpg'.format(imageNumber))
        progress_var.set(step)
        sleep(0.02)
        root.update_idletasks()

def sendEmail():
    link = s3Client.uploadFile("images/image1.jpg", "groupbcreol")
    emailClient.sendScanEmail(name.get(), email.get(), link)

root = Tk(className="3d Scanning System")
root.geometry("400x300")

leftFrame = Frame(root)
leftFrame.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

scanButton = Button(leftFrame, text="Start Scan", command=scan)
scanButton.pack()

progress_var = DoubleVar()
progress_var.set(stepCount)
progressbar = ttk.Progressbar(leftFrame, variable=progress_var, maximum=steps)
progressbar.pack(fill=X, expand=1)

nameLabel = Label(rightFrame, text="Name")
emailLabel = Label(rightFrame, text="Email")
name = StringVar()
email = StringVar()
nameEntry = Entry(rightFrame, textvariable=name)
emailEntry = Entry(rightFrame, textvariable=email)

nameLabel.grid(row=0)
emailLabel.grid(row=1)

nameEntry.grid(row=0, column=1)
emailEntry.grid(row=1, column=1)

sendEmailButton = Button(rightFrame, text="Send Email", command=sendEmail)
sendEmailButton.grid(row=2, columnspan=2)

root.mainloop()
