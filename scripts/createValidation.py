"""
Creates a set of validation images spatially distributed across
the study area orthophoto with a use specified coverage area (%)
and block size?
"""
def createValidation(orthoPath, tileSize, pctTraining):
    # read in orthophoto from path
    img = np.asarray(Image.open(orthoPath))

    # calculate image size and tile sizes
    img.reshape

    # warn if image is not multiple of tile sizes

    # split image into tiles using reshape of numpy array
