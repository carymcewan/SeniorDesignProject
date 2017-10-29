# Corresponds to all the matlab functions in *.m files

import numpy as np
# import matplotlib.pyplot as plt
from scipy import ndimage

# Replaces element vertex value in line 3 of ply file
# Only called for the last set of points to reduce read/writes
def update_vertex_count_ply(updated_vertex_count):
    file = open("matply.ply")
    lines = file.readlines()

    # Element vertex line is always the third line in the file. We split the spaces to get the vertex value
    # ie. if the line is "element vertex 35", we want "35"
    # we then replace this value with our updated vertex count
    element_vertex_line_array = lines[2].split(" ")
    element_vertex_line_array[2] = str(updated_vertex_count)
    new_line = " ".join(element_vertex_line_array) + "\n"
    lines[2] = new_line
    file.close()

    # Now write the original lines back to the file, this time with then updated vertex count
    new_file = open("matply.ply", "w")
    new_file.writelines(lines)
    new_file.close()

def append_ply(point_cloud_data):

    file = open('matply.ply', 'a')
    
    file.write('\n')
    
    for point_cloud in point_cloud_data[:-1]:
        file.write(str.format('{} {} {}\n', point_cloud[0], point_cloud[1], point_cloud[2]))
        
    # Print last coordinate without new line
    last_point = point_cloud_data[-1]
    file.write(str.format('{} {} {}', last_point[0], last_point[1], last_point[2]))
    
    file.close()
    

def init_ply(point_cloud_data):
    
    # Create ply file
    file = open('C:\\Users\\isaias\\Desktop\\matply.ply', 'w')
    
    # Write the file header. 
    
    headers = ['ply\n', 'format ascii 1.0\n', str.format('element vertex {}\n', len(point_cloud_data)), 'property float 32 x\n', 'property float 32 y\n', 'property float 32 z\n', 'end_header\n']
    file.writelines(headers)
    
    for point_cloud in point_cloud_data[:-1]:
        file.write(str.format('{} {} {}\n', point_cloud[0], point_cloud[1], point_cloud[2]))
    
    # Print last coordinate without new line
    last_point = point_cloud_data[-1]
    file.write(str.format('{} {} {}', last_point[0], last_point[1], last_point[2]))
    
    file.close()

# needs to be passed in :to function im = ndimage.imread('buddha2.jpg')

# Returns PCL array with dropped empty columns
def point_detection(image): # takes an ndimage
    im_rotated = ndimage.rotate(image, 180)
        
    start_px = 222
    stop_px = 814
    sample_rate = 2
    
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


def main(filename="image"):
    path = "C:\\Users\\isaias\\Desktop\\images\\"
    # first image only here
    image = ndimage.imread(path + filename + "1 (1).jpg")
    pcl = point_detection(image)
    
    pcl_size = pcl.shape[0]
    # Initialize PlyWriter to wriet PLY file
    with open("C:\\Users\\isaias\\Desktop\\matply.ply",'w') as plyfile:
        
        headers = ['ply\n', 'format ascii 1.0\n', str.format('element vertex {}\n', pcl_size), 'property float 32 x\n', 'property float 32 y\n', 'property float 32 z\n', 'end_header\n']
        for header in headers:
            plyfile.write(header)
        plyfile.write(str.format("{} {} {}", pcl[0], pcl[1], pcl[2]))
    
    
    # Loop through the rest
    for i in range(1,399):
        theta = i*(np.pi/200)
        nim = ndimage.imread(path+filename+str(i)+" (1).jpg")
        pcl = point_detection(nim)
        rot = pcl_rotate(theta,pcl)
        pcl_size = pcl_size + rot.shape[0]
        
        with open("C:\\Users\\isaias\\Desktop\\matply.ply",'a') as plyfile:
            plyfile.write(str.format("{} {} {}", pcl[0], pcl[1], pcl[2]))
   
    # at end
    # write header and ply contents
        
            