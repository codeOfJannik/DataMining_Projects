import matplotlib
from os.path import isdir,join,normpath
from os import listdir
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mplimg
import matplotlib.pyplot as plt
import sys


def parseDirectory(directoryName,extension):
    '''This method returns a list of all filenames in the Directory directoryName.
    For each file the complete absolute path is given in a normalized manner (with
    double backslashes). Moreover only files with the specified extension are returned in
    the list.
    '''
    if not isdir(directoryName): return
    imagefilenameslist=sorted([
        normpath(join(directoryName, fname))
        for fname in listdir(directoryName)
        if fname.lower().endswith('.'+extension)
        ])
    return imagefilenameslist



training_images = '/Users/MontyRock/PycharmProjects/DataMiningProjects/Resources/Gesichtsbilder/training'
test_images = '/Users/MontyRock/PycharmProjects/DataMiningProjects/Resources/Gesichtsbilder/test'
training_image_list = parseDirectory(training_images, 'png')
test_image_list = parseDirectory(test_images, 'png')


def get_average_image(images):
    average = range(len(images[0]))
    for idx in np.arange(len(images[0])):
        array = [x[idx] for x in images]
        average[idx] = np.average(array)
    return np.array(average)


def get_normed_array_of_faces(images, average_image):
    normed = []
    for idx in np.arange(len(images)):
        normed.append(images[idx] - average_image)
    return np.array(normed)


def reshape_image(image, width=150, height=220):
    shaped_image = image.copy()
    shaped_image.shape = (height, width)
    return shaped_image

average_image = get_average_image(training_image_list)
normed_array_of_faces = get_normed_array_of_faces(training_image_list, average_image)


plt.imshow(reshape_image(average_image), cmap='gray')
plt.colorbar()
imgplot = plt.title("Durchschnittsbild", size=15)


def calculateEigenfaces(adjfaces, width=150, height=220):
    eigenvecs_of_CV = []

    reduced_matrix = np.dot(adjfaces, np.transpose(adjfaces))
    M = reduced_matrix.shape[0]

    (eigenval_of_reduced, eigenvecs_of_reduced) = np.linalg.eigh(reduced_matrix)
    print
    "M= " + str(M)
    print
    "adjfaces= " + str(adjfaces.shape)

    for i in range(M):
        u = [0] * adjfaces.shape[1]
        for k in range(M):
            u = u + (eigenvecs_of_reduced[i, k] * adjfaces[k])
        eigenvecs_of_CV.append(u)

    return np.array([eigenvec for _, eigenvec in sorted(zip(eigenval_of_reduced, eigenvecs_of_CV))])


eigenfaces = calculateEigenfaces(normed_array_of_faces)
usub = eigenfaces[:6]

M= 63
adjfaces= (63, 33000)



def readImageToNumpyData(imageList):
    images_list = []
    for image in imageList:
        img = img=mplimg.imread(image)
        pixeldata = np.array(img)
        pixeldata = pixeldata.flatten()
        pixeldata = pixeldata / max(pixeldata)
        images_list.append(pixeldata)
    return np.array(images_list)

training_image_list = readImageToNumpyData(training_image_list)


def get_average_image(images):
    average = range(len(images[0]))
    for idx in np.arange(len(images[0])):
        array = [x[idx] for x in images]
        average[idx] = np.average(array)
    return np.array(average)


def get_normed_array_of_faces(images, average_image):
    normed = []
    for idx in np.arange(len(images)):
        normed.append(images[idx] - average_image)
    return np.array(normed)


def reshape_image(image, width=150, height=220):
    shaped_image = image.copy()
    shaped_image.shape = (height, width)
    return shaped_image


average_image = get_average_image(training_image_list)
normed_array_of_faces = get_normed_array_of_faces(training_image_list, average_image)



plt.imshow(reshape_image(average_image), cmap='gray')
plt.colorbar()
imgplot = plt.title("Durchschnittsbild", size=15)




def calculateOmegaValues(normedArrayOfFaces, eigenspace, verbose=False):
    # Verify
    if (eigenspace.shape[1] == normedArrayOfFaces.shape[1]):
        if (verbose):
            print
            'Same Dimensions'
    else:
        sys.stderr.write('The Matrices do not have the same dimensions')

    # Logic
    omega_value_list = np.zeros((normedArrayOfFaces.shape[0], eigenspace.shape[0]))
    for i, image in enumerate(normedArrayOfFaces):
        for k, es in enumerate(eigenspace):
            # Both vectors are supplied horizontal
            # dot product expects h*v to calculate a single value
            omega_i_k = np.dot(es, np.transpose(image))
            omega_value_list[i, k] = omega_i_k

    return omega_value_list
