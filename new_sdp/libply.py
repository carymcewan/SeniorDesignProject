from util import *
import numpy as np
import cv2
PATH_PLY = "/home/isaias/Documents/tape_ball.ply"
PATH_IMAGES = "/home/isaias/Pictures/imagesTapeBall/"




def init_ply():
    # Write the file header. 
    headers = ['ply\n', 'format ascii 1.0\n', 'element vertex 0\n', 
               'property float32 x\n', 'property float32 y\n',
               'property float32 z\n', 'end_header']
               
    # Create ply file
    with open(PATH_PLY, 'w') as file:
        file.writelines(headers)
        
def pcl_rotate(theta, pcl_arr):
    r = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])
                  
    return r.dot(pcl_arr)

def load_image(path):
    image = cv2.imread(path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def append_ply(pcl):

    with open(PATH_PLY, 'a') as file:
        file.write('\n')
        
        length = pcl.shape[1]
        for index in range(length-1):
            x = pcl[0][index]
            y = pcl[1][index]
            z = pcl[2][index]
            
            file.write("{} {} {}\n".format(x, y, z))
            
        last_x = pcl[0][-1]
        last_y = pcl[1][-1]
        last_z = pcl[2][-1]
        file.write("{} {} {}".format(last_x, last_y, last_z))

def update_vertex_count_ply(updated_vertex_count):

    file = open(PATH_PLY)

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
    new_file = open(PATH_PLY, "w")
    new_file.writelines(lines)
    new_file.close()


def r_rgb(image):
    return cv2.split(image)[0]

def point_detection(image1, image2):

    #imlaser = r_rgb(np.rot90(np.rot90(image1)))
    #imbk = r_rgb(np.rot90(np.rot90(image2)))
    #r, g, b = cv2.split(im_rotated)
    #imsub = cv2.subtract(r, cv2.divide(cv2.add(g, b), 2))

    imlaser = r_rgb(image1)
    imbk = r_rgb(image2)

    imsub = r_rgb(cv2.subtract(imlaser,imbk))

    start_px = 0
    stop_px = imsub.shape[0]
    sample_rate = 2
    threshold = 30
    
    threshold = np.uint8(threshold)
    
    pcl = np.zeros((3,5000))
    
    pcl_count = 0
    y = 0

    for z in range(start_px, stop_px, sample_rate):
        intensity = np.amax(imsub[z,:])
        
        if intensity > threshold:
            x = np.argmax(imsub[z,:])
            pcl[:, pcl_count] = np.array([x,y,z])
            pcl_count += 1
    return pcl[:, :pcl_count]


def main():

    init_ply()
    vcount = 0
    
    # bigPCL = np.zeros(0)
    
    for i in range(1, 401):

        imfile = PATH_IMAGES + "image" + str(i) + ".jpg"
        imfile2 = PATH_IMAGES + "image" + str(i) + "_laserOff.jpg"
        theta = (i)*(np.pi/200)

        image_laser = load_image(imfile)
        image_bk = load_image(imfile2)

        pcl = point_detection(image_laser, image_bk)
        
        diff = np.zeros((3, pcl.shape[1]))
        
        diff[0].fill(1751)
        
        pcl -= diff
        
        rot = pcl_rotate(theta, pcl)
                
        # Save us time from opening a file if there aren't any points to write.
        if rot.size != 0:
            append_ply(rot)
            
        vcount += pcl.shape[1]
        #print("Processed image DOG {} with {} points.".format(i, rot.shape[1]))

    update_vertex_count_ply(vcount)
