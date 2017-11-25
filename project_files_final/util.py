import cv2
import math
import pylab
import struct
import datetime
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

_begin = 0
total_time = datetime.timedelta()

# Time measurement functions

def begin():
    global _begin
    _begin = datetime.datetime.now()


def end():
    global _begin, total_time
    end = datetime.datetime.now() - _begin
    total_time += end
    print('Time: %s' % end)


def total():
    global total_time
    print('Total time: %s' % total_time)


# Plot image functions

def plot_image(image):
    if len(image.shape) == 2:
        image = cv2.merge((image, image, image))
    f, axarr = plt.subplots(1, 1, figsize=(10, 15))
    axarr.axis('off')
    axarr.imshow(image)
    axarr.plot()


def plot_images(images):
    f, axarr = plt.subplots(1, len(images), figsize=(15, 15))
    for i in range(len(images)):
        if len(images[i].shape) == 2:
            image = cv2.merge((images[i], images[i], images[i]))
        else:
            image = images[i]
        axarr[i].axis('off')
        axarr[i].imshow(image)
        axarr[i].plot()


# Load image function

def load_image(path):
    image = cv2.imread(path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


