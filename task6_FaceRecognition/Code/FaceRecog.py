# %matplotlib inline
from os.path import isdir, join, normpath
from os import listdir
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mplimg


def parseDirectory(directoryName, extension):
    '''This method returns a list of all filenames in the Directory directoryName.
    For each file the complete absolute path is given in a normalized manner (with
    double backslashes). Moreover only files with the specified extension are returned in
    the list.
    '''
    if not isdir(directoryName): return
    imagefilenameslist = sorted([
        normpath(join(directoryName, fname))
        for fname in listdir(directoryName)
        if fname.lower().endswith('.' + extension)
    ])
    return imagefilenameslist


imagefilenamelist = parseDirectory(
    "/Users/janniks97/Documents/DataMining/DataMiningProjects/Resources/Gesichtsbilder/training", "png")
print(imagefilenamelist)


def readImageToNumpyData(imageList):
    serializedImages = np.empty((0, 33000))
    for image in imageList:
        img = mplimg.imread(image)
        img.shape = (1, -1)
        maxValue = np.amax(img)
        img = img / maxValue
        serializedImages = np.append(serializedImages, img, axis=0)
    return serializedImages


imageList = readImageToNumpyData(imagefilenamelist)


def calculateAverageImage(imageList):
    return np.average(imageList, axis=0)


averageImage = calculateAverageImage(imageList)


def createNormedFacesArray(imageList, averageImage):
    return imageList - averageImage


normedArrayOfFaces = createNormedFacesArray(imageList, averageImage)


def showImage(imageVector):
    img = np.reshape(imageVector, (220, 150))
    plt.imshow(img)


showImage(averageImage)


def calculateEigenfaces(adjfaces, width, height):
    CV = np.dot(np.transpose(adjfaces), adjfaces)
    return np.linalg.eigh(CV)


eigenvalues, eigenvectors = calculateEigenfaces(normedArrayOfFaces, 220, 150)
