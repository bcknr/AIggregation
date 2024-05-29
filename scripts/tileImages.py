"""
Function for splitting images into tiles of specified size. If main image cant be tiled perfectly
images will overlap at the edges. Can also specify overlap for all images.

To run specify 
- path to image folder
- path to output folder
- tile dimensions
- overlap amount

"""

#import modules
import cv2
import glob
import os
from PIL import Image

# set tile dimensions
split_width = 608
split_height = 608

# set overlap between images (value from 0 to 1)
overlap_amount = 0

# set input image folder
path_to_img = "input/drone_photos/training/*.jpg"

#set output folder
output_path = "input/drone_photos/training_split"



def start_points(size, split_size, overlap=0):
    points = [0]
    stride = int(split_size * (1-overlap))
    counter = 1
    while True:
        pt = stride * counter
        if pt + split_size >= size:
            if split_size == size:
                break
            points.append(size - split_size)
            break
        else:
            points.append(pt)
        counter += 1
    return points



for filename in glob.glob(path_to_img):

    img_dim = Image.open(filename)
    img_h = img_dim.height
    img_w = img_dim.width
    img = cv2.imread(filename)
    img_h, img_w, _ = img.shape

    X_points = start_points(img_w, split_width, overlap_amount)
    Y_points = start_points(img_h, split_height, overlap_amount)

    count = 0
    name = os.path.join(output_path, os.path.basename(filename))
    frmt = 'jpeg'

    for i in Y_points:
        for j in X_points:
            split = img[i:i+split_height, j:j+split_width]
            cv2.imwrite('{}_{}.{}'.format(name, count, frmt), split)
            count += 1
