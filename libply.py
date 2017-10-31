# Corresponds to all the matlab functions in *.m files

import numpy as np
from scipy import ndimage

PATH_PLY = "cylinder.ply"
PATH_IMAGES = "imagesCylinder/"

# Replaces element vertex value in line 3 of ply file
# Only called for the last set of points to reduce read/writes
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
    

def init_ply():
    # Write the file header. 
    headers = ['ply\n', 'format ascii 1.0\n', 'element vertex 0\n', 
               'property float32 x\n', 'property float32 y\n',
               'property float32 z\n', 'end_header']
               
    # Create ply file
    with open(PATH_PLY, 'w') as file:
        file.writelines(headers)

# Returns PCL array with dropped empty columns
def point_detection(image):

    im_rotated = np.rot90(image)
    im_rotated = np.rot90(im_rotated)

    start_px = 0
    stop_px = 1868
    sample_rate = 2
    threshold = 50
    
    pcl = np.zeros((3,2500))
    
    pcl_count = 0
    y = 0
        
    ir = im_rotated[:, :, 0]
    ig = im_rotated[:, :, 1]
    ib = im_rotated[:, :, 2]

    im_rotated = ir - ((ig + ib) / 2)
    
    for z in range(start_px, stop_px, sample_rate):
        intensity = np.amax(im_rotated[z,:])
        
        if intensity > np.uint8(threshold):
            x = np.argmax(im_rotated[z,:])
            pcl[:, pcl_count] = np.array([x,y,z])
            pcl_count = pcl_count + 1
            
    return pcl[:, :pcl_count]
    
        
def pcl_rotate(theta, pcl_arr):
    r = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])
                  
    return r.dot(pcl_arr)


def main():

    init_ply()
    vcount = 0
    
    for i in range(1, 401):

        imfile = PATH_IMAGES + "image" + str(i) + ".jpg"

        theta = (i-1)*(np.pi/200)

        nim = ndimage.imread(imfile)

        pcl = point_detection(nim)
        
        rot = pcl_rotate(theta, pcl)

        diff = np.zeros((3, pcl.shape[1]))
        
        diff[0].fill(1751)

        rot -= diff
        
        # Save us time from opening a file if there aren't any points to write.
        if rot.size != 0:
            append_ply(rot)
            
        vcount += pcl.shape[1]
        print("Processed image {} with {} points.".format(i, rot.shape[1]))

    update_vertex_count_ply(vcount)

if __name__ == "__main__":
    main()