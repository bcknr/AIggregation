"""
Function for splitting images into tiles of specified size allowing for overlap.
If images overlap they are randomly rotated and flipped so that any nests that
are shared between two images can still be used in the training dataset.
"""

def tileImages(img, width, height):
     # Load image
     # Get size and calc overlap
     # tile image
     # assign random flip/rotation 
     # export as tiles