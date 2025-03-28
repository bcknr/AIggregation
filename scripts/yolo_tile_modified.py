
'''

Python script modified from slanj

https://github.com/slanj/yolo-tiling/blob/main/tile_yolo.py

This should take the large yolo output and tile it, creating seperate smaller images and label files. 



'''



import pandas as pd
import numpy as np
from PIL import Image
from shapely.geometry import Polygon
import glob
import argparse
import os
import random
import yaml 


def tiler(imnames, newpath, allimages, slice_size, ext):

    for imname in imnames:
        im = Image.open(imname)
        imr = np.array(im, dtype=np.uint8)
        height = imr.shape[0]
        width = imr.shape[1]
        labname = imname.replace(ext, '.txt').replace('images', 'labels')
        labels = pd.read_csv(labname, sep=' ', names=['class', 'x1', 'y1', 'w', 'h', 'conf'])
        
        # we need to rescale coordinates from 0-1 to real image height and width
        labels[['x1', 'w']] = labels[['x1', 'w']] * width
        labels[['y1', 'h']] = labels[['y1', 'h']] * height
        
        boxes = []
        
        # convert bounding boxes to shapely polygons. We need to invert Y and find polygon vertices from center points
        for row in labels.iterrows():
            x1 = row[1]['x1'] - row[1]['w']/2
            y1 = (height - row[1]['y1']) - row[1]['h']/2
            x2 = row[1]['x1'] + row[1]['w']/2
            y2 = (height - row[1]['y1']) + row[1]['h']/2
            conf = row[1]['conf']

            boxes.append((int(row[1]['class']), Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)]), conf))
        
        counter = 0
        print('Image:', imname)
        print(boxes)

        # create tiles and find intersection with bounding boxes for each tile
        for i in range((height // slice_size)):
            for j in range((width // slice_size)):
                x1 = j*slice_size
                y1 = height - (i*slice_size)
                x2 = ((j+1)*slice_size) - 1
                y2 = (height - (i+1)*slice_size) + 1

                pol = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
                imsaved = False
                slice_labels = []

                for box in boxes:
                    if pol.intersects(box[1]):
                        inter = pol.intersection(box[1])        
                        
                        if not imsaved:
                            sliced = imr[i*slice_size:(i+1)*slice_size, j*slice_size:(j+1)*slice_size]
                            sliced_im = Image.fromarray(sliced)
                            filename = imname.split('/')[-1]
                            slice_path = newpath + "/images/" + filename.replace(ext, f'_{i}_{j}{ext}')                            
                            slice_labels_path = newpath + "/labels/" + filename.replace(ext, f'_{i}_{j}.txt')                            
                            print(slice_path)
                            # could add if statement here for selective save
                            sliced_im.save(slice_path)
                            imsaved = True                    
                        
                        # get smallest rectangular polygon (with sides parallel to the coordinate axes) that contains the intersection
                        new_box = inter.envelope 
                        
                        # get central point for the new bounding box 
                        centre = new_box.centroid
                        
                        # get coordinates of polygon vertices
                        x, y = new_box.exterior.coords.xy
                        
                        # get bounding box width and height normalized to slice size
                        new_width = (max(x) - min(x)) / slice_size
                        new_height = (max(y) - min(y)) / slice_size
                        
                        # we have to normalize central x and invert y for yolo format
                        new_x = (centre.coords.xy[0][0] - x1) / slice_size
                        new_y = (y1 - centre.coords.xy[1][0]) / slice_size
                        
                        counter += 1

                        print(box)
                        print(box[2])

                        slice_labels.append([box[0], new_x, new_y, new_width, new_height, box[2] ])
                
                if len(slice_labels) > 0:
                    slice_df = pd.DataFrame(slice_labels, columns=['class', 'x1', 'y1', 'w', 'h', 'conf'])
                    print(slice_df)
                    slice_df.to_csv(slice_labels_path, sep=' ', index=False, header=False, float_format='%.6f')
                
                if not imsaved and allimages:
                    sliced = imr[i*slice_size:(i+1)*slice_size, j*slice_size:(j+1)*slice_size]
                    sliced_im = Image.fromarray(sliced)
                    filename = imname.split('/')[-1]
                    slice_path = newpath + "/images/" + filename.replace(ext, f'_{i}_{j}{ext}')                
                    sliced_im.save(slice_path)
                    print('Slice without boxes saved')
                    imsaved = True

def splitter(target, ext, ratio, overwrite):


        
    # check if we want to create a new set of test files 
    # or create tiles based on an existing list
    if overwrite == "TRUE":

        # pull image names
        imnames = glob.glob(f'{target}/images/*{ext}')
        names= [name.split('/')[-1].split('.')[0] for name in imnames]

        # create lists for nontest and test images
        nontest = []
        test = []
        fulllist = []
        test_list = (random.sample(names, k=round(len(names)*ratio)))

        # modify with random
        for name in names:
            fulllist.append(os.path.join(name + ext))
            fulllist.append(os.path.join(name + ".txt"))
            if name in test_list:
                test.append(os.path.join(name + ext))
                test.append(os.path.join(name + ".txt"))
            else:
                nontest.append(os.path.join(name + ext))
                nontest.append(os.path.join(name + ".txt"))
        print('train:', len(nontest))
        print('test:', len(test))

        # we will put test.txt, nontest.txt in main folder with yaml

        # write nontest list to txt
        with open(f'{target}/nontest.txt', 'w') as f:
            for item in nontest:
                f.write("%s\n" % item)

        # write test list 
        with open(f'{target}/test.txt', 'w') as f:
            for item in test:
                f.write("%s\n" % item)

        # write full list  
        with open(f'{target}/full_list.txt', 'w') as f:
            for item in fulllist:
                f.write("%s\n" % item)

    # if overwrite = FALSE, read list of nontest and delete those images
    else:
        with open(f'{target_upfolder}/nontest.txt', 'r') as f:
            nontest = [line.strip() for line in f]

    # now we delete all images and labels that are in the nontest list 
    for f in nontest:
            full_file_path = glob.glob(f'{target}/*/{f}*')
            for file in full_file_path:
                os.remove(file)




# yaml creation
def yamlizer(target):

    folder = target.split('/')[-1] # get end of string (folder name)

    data = {
        'names':{
        0: "nest"},
        'path': os.path.join("..", folder),
        'val': "./images/"
            }
    with open((os.path.join(target,"dataset.yaml")), 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, sort_keys=False)







if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-source", default="./datasets/export_predictions/", help = "Source folder with images and labels needed to be tiled")
    parser.add_argument("-target", default="./datasets/testset/", help = "Target folder for a new sliced dataset")
    parser.add_argument("-ext", default=".JPG", help = "Image extension in a dataset. Default: .JPG")
    parser.add_argument("-all_images", default= "TRUE", help = "Folder for tiles without bounding boxes")
    parser.add_argument("-size", type=int, default=608, help = "Size of a tile. Default: 608")
    parser.add_argument("-ratio", type=float, default=0.2, help = "Train/test split ratio. Default: 0.2")
    parser.add_argument("-overwrite", default="FALSE", help = "overwrites and creates new training set instead of pulling from existing txt called testlist. default: FALSE")


    args = parser.parse_args()

    imnames = glob.glob(f'{args.source}/images/val/*{args.ext}')
    labnames = glob.glob(f'{args.source}/labels/val/*.txt')

    
    if len(imnames) == 0:
        raise Exception("Source folder should contain some images")
    elif len(imnames) != len(labnames):
        raise Exception("Dataset should contain equal number of images and txt files with labels")

    if not os.path.exists(args.target):
        os.makedirs(args.target)
        os.makedirs(os.path.join(args.target,"images/"))
        os.makedirs(os.path.join(args.target,"labels/"))
    elif len(os.listdir(args.target)) > 0:
        raise Exception("Target folder should be empty")
    
    upfolder = os.path.join(args.source, '..' )
    target_upfolder = os.path.join(args.target, '..' )

 

    tiler(imnames, args.target, args.all_images, args.size, args.ext)
    splitter(args.target, args.ext, args.ratio, args.overwrite)
    yamlizer(args.target)
    