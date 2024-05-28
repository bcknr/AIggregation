""" test script for tiling images with overlap - messy playground

code taken from https://github.com/Devyanshu/image-split-with-overlap

testing with image 1920x1157

needed for script 
- cv2
    $ pip install opencv-python opencv-python-headless
- Pillow == extract image dimensions
- math == to find common factor
"""

#import modules
import cv2
from PIL import Image

path_to_img = "input/test_files/tile_test_nests.jpg"

img_pil = Image.open(path_to_img) 
img_h = img_pil.height 
img_w = img_pil.width 

img = cv2.imread(path_to_img)
img_h, img_w, _ = img.shape
split_width = 608
split_height = 608


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


#adjust the overlap percent 
X_points = start_points(img_w, split_width, 0)
Y_points = start_points(img_h, split_height, 0)

count = 0
name = 'input/test_files/split/split'
frmt = 'jpeg'

for i in Y_points:
    for j in X_points:
        split = img[i:i+split_height, j:j+split_width]
        cv2.imwrite('{}_{}.{}'.format(name, count, frmt), split)
        count += 1

