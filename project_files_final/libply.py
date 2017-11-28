import cv2
import numpy as np

PATH_PLY = "scan.ply"
PATH_IMAGES ="images/"

#camera_matrix 
K = np.array(
    [[  3.24171244e+03,   0.00000000e+00,   1.06029763e+03],
     [  0.00000000e+00,   3.25977353e+03,   1.94331846e+03],
     [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])

distortion_coefficients = np.array([0.47016272, 0.398826, 0.08195973, -0.05850632, -0.67014709])


fx = K[0][0]
fy = K[1][1]
cx = K[0][2]
cy = K[1][2]

def vflip_image(image):
    return cv2.flip(image, 0)

def hflip_image(image):
    return cv2.flip(image, 1)

def init_ply(path_ply=PATH_PLY):
    # Write the file header. 
    headers = ['ply\n', 'format ascii 1.0\n', 'element vertex 0\n', 
               'property float32 x\n', 'property float32 y\n',
               'property float32 z\n', 'end_header']
               
    # Create ply file
    with open(path_ply, 'w') as file:
        file.writelines(headers)
        
def pcl_rotate(theta, pcl_arr):
    r = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])
                  
    return r.dot(pcl_arr)

def load_image(path):
    image = cv2.imread(path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def append_ply(pcl, path_ply=PATH_PLY):

    with open(path_ply, 'a') as file:
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

def update_vertex_count_ply(updated_vertex_count, path_ply=PATH_PLY):

    file = open(path_ply)

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
    new_file = open(path_ply, "w")
    new_file.writelines(lines)
    new_file.close()


def r_rgb(image):
    return cv2.split(image)[0]

def point_detection(imlaser, imbk):
    
    # image subtraction and channel subtraction
    imsub = cv2.subtract(imlaser, imbk)
    r, g, b = cv2.split(imsub)
    imsub = cv2.subtract(r, cv2.divide(cv2.add(g, b), 2))

    # rotation
    imsub = vflip_image(imsub)
    imsub = hflip_image(imsub)


    start_px = 0
    stop_px = imsub.shape[0]
    sample_rate = 2
    threshold = np.uint8(25)
    
    pcl = np.zeros((3,2500))
    
    pcl_count = 0
    y = 0

    for z in range(start_px, stop_px, sample_rate):
        intensity = np.amax(imsub[z,:])
        
        if intensity > threshold:
            x = np.argmax(imsub[z,:])
            pcl[:, pcl_count] = np.array([x,y,z])
            pcl_count += 1
    return pcl[:, :pcl_count]
                      
def main(path_images=PATH_IMAGES, path_ply=PATH_PLY):

    init_ply(path_ply=path_ply)
    vcount = 0
    
    for i in range(1, 401):

        imfile = path_images + "image" + str(i) + ".jpg"
        imfile2 = path_images + "image" + str(i) + "_laserOff.jpg"

        image_laser = load_image(imfile)
        image_bk = load_image(imfile2)

        theta = (i)*(np.pi/200)

        pcl = point_detection(image_laser, image_bk)
        
        diff = np.zeros((3, pcl.shape[1]))
        
        diff[0].fill(750)
        
        pcl -= diff
        
        rot = pcl_rotate(theta, pcl)
                
        # Save us time from opening a file if there aren't any points to write.
        if rot.size != 0:
            append_ply(rot, path_ply=path_ply)
            
        vcount += pcl.shape[1]
        print("Processed image {} with {} points.".format(i, rot.shape[1]))

    update_vertex_count_ply(vcount, path_ply=path_ply)

def load_ply(filename):
    with open(filename, 'r') as f:
        line = None
        header = ''
        while line != 'end_header\n' and line != '':
            line = f.readline()
            header += line

        data = f.readlines()
        data = [l.split()[:3] for l in data]
        data = [tuple(l) for l in data]

        return np.array(data, dtype=np.float64)