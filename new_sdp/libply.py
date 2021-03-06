from util import *
import numpy as np
import cv2

PATH_PLY = "/home/isaias/Pictures/laser.ply"
PATH_IMAGES ="/home/isaias/Pictures/checkerboardRotation/"

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

def pattern_detection(image):
    rows, columns, square_width = 5, 9, 17
    # Convert image to 1 channel
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (columns, rows), flags=cv2.CALIB_CB_FAST_CHECK)

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Find corners with subpixel accuracy
    cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    return corners, ret

def draw_pattern(image, corners, ret):
    rows, columns, square_width = 5, 9, 17
    # Draw corners into image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.drawChessboardCorners(image, (columns, rows), corners, ret)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image

def point_detection(image1, image2):


    imlaser = r_rgb(image1)
    imbk = r_rgb(image2)

    imsub = r_rgb(cv2.subtract(imlaser,imbk))


    start_px = 0
    stop_px = imsub.shape[0]
    sample_rate = 2
    threshold = np.uint8(30)
    
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

def roi_point_detection(image1, image2):
    rows, columns, square_width = 5, 9, 17
    h, w, d = image1.shape

    corners, ret = pattern_detection(image1)
    corners = corners.astype(np.int)
        
    p1 = corners[0][0]
    p2 = corners[columns - 1][0]
    p3 = corners[columns * (rows - 1)][0]
    p4 = corners[columns * rows - 1][0]

    # Compute ROI

    roi_mask = np.zeros((h, w), np.uint8)
    points = np.array([p1, p2, p4, p3])
    cv2.fillConvexPoly(roi_mask, points, 255)

    image_laser = r_rgb(image1)
    image_background = r_rgb(image2)
    
    image_sub = r_rgb(cv2.subtract(image_laser, image_background))
    image_sub = cv2.bitwise_and(image_sub, roi_mask)  
    
    threshold_value = 30
    image_threshold = cv2.threshold(image_diff_r, threshold_value, 255, cv2.THRESH_TOZERO)[1]

    # Blur image

    blur_value = 5
    image_blur = cv2.blur(image_threshold, (blur_value, blur_value))

    image_blur_threshold = cv2.threshold(image_blur, threshold_value, 255, cv2.THRESH_TOZERO)[1]


    window = 4
    peak = image_blur_threshold.argmax(axis=1)
    _min = peak - window
    _max = peak + window + 1
    mask = np.zeros_like(image_blur_threshold)

    for i in range(image_blur_threshold.shape[0]):
        mask[i, _min[i]:_max[i]] = 255

    image_stripe = cv2.bitwise_and(image_sub, mask)

    data = np.vstack((v.ravel(), u.ravel())).T
    model, inliers = ransac(data, LinearLeastSquares2D(), 2, 2)

    dr, thetar = model
    f = (dr - v * math.sin(thetar)) / math.cos(thetar)

    image_stripe = cv2.merge((cv2.add(image_diff_r, image_line_lr), image_line_lr, image_line_lr))

    image_stripe_r = r_rgb(image_stripe)

    start_px = 0
    stop_px = image_stripe_r.shape[0]
    sample_rate = 2
    threshold = np.uint8(30)

    pcl = np.zeros((3,5000))

    pcl_count = 0
    y = 0

    for z in range(start_px, stop_px, sample_rate):
        intensity = np.amax(image_stripe_r[z,:])

        if intensity > threshold:
            x = np.argmax(image_stripe_r[z,:])
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


class LinearLeastSquares2D(object):
    '''
    2D linear least squares using the hesse normal form:
        d = x*sin(theta) + y*cos(theta)
    which allows you to have vertical lines.
    '''

    def fit(self, data):
        data_mean = data.mean(axis=0)
        x0, y0 = data_mean
        if data.shape[0] > 2:  # over determined
            u, v, w = np.linalg.svd(data - data_mean)
            vec = w[0]
            theta = math.atan2(vec[0], vec[1])
        elif data.shape[0] == 2:  # well determined
            theta = math.atan2(data[1, 0] - data[0, 0], data[1, 1] - data[0, 1])
        theta = (theta + math.pi * 5 / 2) % (2 * math.pi)
        d = x0 * math.sin(theta) + y0 * math.cos(theta)
        return d, theta

    def residuals(self, model, data):
        d, theta = model
        dfit = data[:, 0] * math.sin(theta) + data[:, 1] * math.cos(theta)
        return np.abs(d - dfit)

    def is_degenerate(self, sample):
        return False

def ransac(data, model_class, min_samples, threshold, max_trials=100):
    '''
    Fits a model to data with the RANSAC algorithm.
    :param data: numpy.ndarray
        data set to which the model is fitted, must be of shape NxD where
        N is the number of data points and D the dimensionality of the data
    :param model_class: object
        object with the following methods implemented:
         * fit(data): return the computed model
         * residuals(model, data): return residuals for each data point
         * is_degenerate(sample): return boolean value if sample choice is
            degenerate
        see LinearLeastSquares2D class for a sample implementation
    :param min_samples: int
        the minimum number of data points to fit a model
    :param threshold: int or float
        maximum distance for a data point to count as an inlier
    :param max_trials: int, optional
        maximum number of iterations for random sample selection, default 100
    :returns: tuple
        best model returned by model_class.fit, best inlier indices
    '''

    best_model = None
    best_inlier_num = 0
    best_inliers = None
    data_idx = np.arange(data.shape[0])
    for _ in range(max_trials):
        sample = data[np.random.randint(0, data.shape[0], 2)]
        if model_class.is_degenerate(sample):
            continue
        sample_model = model_class.fit(sample)
        sample_model_residua = model_class.residuals(sample_model, data)
        sample_model_inliers = data_idx[sample_model_residua < threshold]
        inlier_num = sample_model_inliers.shape[0]
        if inlier_num > best_inlier_num:
            best_inlier_num = inlier_num
            best_inliers = sample_model_inliers
    if best_inliers is not None:
        best_model = model_class.fit(data[best_inliers])
    return best_model, best_inliers
