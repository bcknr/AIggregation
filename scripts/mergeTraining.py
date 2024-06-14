"""
Renames and merge training image files from LabelStudio into single 
directory will shared names.
"""

import os
import zipfile
import tempfile


def mergeTraining(dest, path=None):
    if path is None:
        path = input("Path to training image directory:")
    else: 
        print(f"Merging files from {path}")
    
    # Create destination directory
    os.makedirs(os.path.join(dest, 'images'))
    os.mkdir(os.path.join(dest,'labels'))

    # Iterate through zip files
    files = os.listdir(path)
    for i,zip in enumerate(files):
        zf = zipfile.ZipFile(os.path.join(path, zip), "r")
        with tempfile.TemporaryDirectory() as tempdir:
            zf.extractall(tempdir)
            
            images = os.listdir(os.path.join(tempdir, "images"))
            labels = os.listdir(os.path.join(tempdir, "labels"))

            # Remove extra file ext if it exists and move other ext to end, move to final dest
            for img in images:
               # if all([x in img for x in ['jpg','jpeg']]):
                newName = os.path.join(dest, "images", img.rstrip('.jpeg').replace('.jpg', '') + '.jpg')
                os.rename(os.path.join(tempdir, "images",img), newName)
            for lbl in labels:
                lblName = os.path.join(dest, "labels", lbl.replace('.jpg', ''))
                os.rename(os.path.join(tempdir, "labels",lbl), lblName)
            
            # Copy metadata files from first script to dest if they don't exist
            if i == 0:
                os.rename(os.path.join(tempdir, "classes.txt"), os.path.join(dest, "classes.txt"))
                os.rename(os.path.join(tempdir, "notes.json"), os.path.join(dest, "notes.json"))
    
        



        


