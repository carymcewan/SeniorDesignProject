import cv2
import numpy as np
import glob
import sys


class Calibrator:
    def __init__(self):
        self._square_size = 22  # mm
        self._pattern_size = (9, 7)
        self._pattern_points = None
        # self._data = CalibrationData()
        self._obj_points = []
        self._img_points = []
        self.cmat = []
        self.dist_coefs = []
        self.rmat = []
        self.tmat = []
        self.mean_error = 0.0

    @property
    def _calculate_pattern_points(self):
        pattern_points = np.zeros((np.prod(self._pattern_size), 3), np.float32)
        pattern_points[:, :2] = np.indices(self._pattern_size).T.reshape(-1, 2)
        pattern_points *= self._square_size
        return pattern_points

    def set_square_size(self, value):
        self._square_size = value

    def set_pattern_size(self, value):
        self._pattern_size = value

    def initialize(self, filenames):
        count = 0
        obj_points, img_points = [], []
        self._pattern_points = self._calculate_pattern_points

        for fn in filenames:
            count += 1

            image = cv2.imread(fn, 0)

            if image is None:
                print("Failed to load", fn)
                continue

            h, w = image.shape[:2]

            found, corners = cv2.findChessboardCorners(image, self._pattern_size)

            if found:
                term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.001)
                cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), term)

            img_points.append(corners.reshape(-1, 2))
            obj_points.append(self._pattern_points)

        self._img_points = img_points
        self._obj_points = obj_points

        rms, camera_matrix, \
        dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
        mean_error = self.calculate_mean_error()

        self._set_calibration_data(camera_matrix, dist_coefs, rvecs, tvecs, mean_error)

    def _set_calibration_data(self, cmat, dist_coefs, rmat, tmat, mean_error):
        self.cmat = cmat
        self.dist_coefs = dist_coefs
        self.rmat = rmat
        self.tmat = tmat
        self.mean_error = mean_error

    def get_calibration_data(self):
        return self.cmat, self.dist_coefs, self.rmat, self.tmat

    def _calculate_mean_error(self):

        total_error = 0

        for i in range(len(self._obj_points)):
            img_points2, _ = cv2.projectPoints(self._obj_points[i], self.rmat[i],
                                               self.tmat[i], self.cmat,
                                               self.dist_coefs)
            img_points2 = img_points2.reshape(-1, 2)
            error = cv2.norm(self._img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
            total_error += error

        return total_error / len(self._obj_points)


    def save_calibrations(self, filename):  # "/home/isaias/Documents/calibration_data.npz"
        np.savez(filename, cmat=self.cmat, dist_coefs=self.dist_coefs, rmat=self.rmat, tmat=self.tmat, mean_error=self.mean_error)

    def load_calibrations(self, filename):
        data = np.load(filename)
        self.cmat = data['cmat']
        self.dist_coefs = data['dist_coefs']
        self.rmat = data['rmat']
        self.tmat = data['tmat']
        self.mean_error = data['mean_error']

if __name__ == "__main__":
    calibrator = Calibrator()
    filenames = glob.glob(sys.argv[1]) # pass dir of calibration images
    calibrator.initialize(filenames)

