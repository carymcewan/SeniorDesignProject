# Corresponds to all the matlab functions in *.m files

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

def append_ply(point_cloud_data):

    file = open('matply.ply', 'a')
    
    file.write('\n')
    
    for point_cloud in point_cloud_data[:len(point_cloud_data)-1]:
        file.write(str.format('{} {} {}\n', point_cloud[0], point_cloud[1], point_cloud[2]))
        
    # Print last coordinate without new line
    last_point = point_cloud_data[len(point_cloud_data) - 1]
    file.write(str.format('{} {} {}', last_point[0], last_point[1], last_point[2]))
    
    file.close()
    

def init_ply(point_cloud_data):
    
    # Create ply file
    file = open('matply.ply', 'w')
    
    # Write the file header. 
    
    headers = ['ply\n', 'format ascii 1.0\n', str.format('element vertex {}\n', len(point_cloud_data)), 'property float 32 x\n', 'property float 32 y\n', 'property float 32 z\n', 'end_header\n']
    for header in headers:
        file.write(header)
    
    for point_cloud in point_cloud_data[:len(point_cloud_data)-1]:
        file.write(str.format('{} {} {}\n', point_cloud[0], point_cloud[1], point_cloud[2]))
    
    # Print last coordinate without new line
    last_point = point_cloud_data[len(point_cloud_data) - 1]
    file.write(str.format('{} {} {}', last_point[0], last_point[1], last_point[2]))
    
    file.close()

# needs to be passed in :to function im = ndimage.imread('buddha2.jpg')

# Returns PCL array with dropped empty columns
def point_detection(image): # takes an ndimage

    im_rotated = ndimage.rotate(image, 180)
        
    start_px = 739
    stop_px = 1559
    sample_rate = 10
    
    pcl = np.zeros((3,500))
    
    pcl_count = 0
    y = 0
        
    ir = im_rotated[:,:,0] 
    ig = im_rotated[:,:,1] 
    ib = im_rotated[:,:,2] 
        
    im_rotated = ir - ((ig + ib) / 2)
    # Find the x coordinate of a pixel, using Z and Y = 0
    # The x coordinate is assigned by finding the index of the max
    # value of each row Z.
    for z in range(start_px, stop_px, sample_rate):
        x = np.argmax(im_rotated[z,:])
        #print("THESE ARE VALS: {}, {},{}".format(x,y,z))
        # Test intensity of pixel if the max brightness is above
        # the threshold 
        if x > np.uint8(50):
            pcl[:,pcl_count] = np.array([x,y,z])
            pcl_count = pcl_count + 1

    return pcl[:,:pcl_count]
    
        
def pcl_rotate(theta, pcl_arr):
    r = np.array([[np.cos(theta), -np.sin(theta),0],
                  [np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])
                  
    return r.dot(pcl_arr)
