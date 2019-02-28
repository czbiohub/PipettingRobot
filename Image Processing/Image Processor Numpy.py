from PIL import Image
import glob
import pyqtgraph as pg
import numpy as np

images = glob.glob('./images/Testing_Images/*.jpg') #Get full path of image folder

def Average(array):
    return np.mean(array, axis=2) #dimensions should be tuple of axis to average

def Flatten(list_of_lists):
    flattened_list = []
    for lst in list_of_lists:
        for item in lst:
            flattened_list.append(item)
    return flattened_list 

def Grayscale(imgarray, weights = np.c_[0.2989, 0.5870, 0.1140]):
    tile = np.tile(weights, reps=(imgarray.shape[0], imgarray.shape[1], 1)) #create a new array that is the same size as image array. new array consists of multipliers for every pixel according to the weights given.
    return np.sum(tile * imgarray, 2) #multiply pixel values in image array with weights from newly created array

def Split_channels(imgarray):
    imgB = imgarray[:,:,0]
    imgG = imgarray[:,:,1]
    imgR = imgarray[:,:,2]
    return imgB, imgG, imgR

def Process():
    for image in sorted(images):
        with open(image, 'rb') as file:
            imgfull = Image.open(file)
            ndimg = np.array(imgfull) #open as ndarray
            # (Image.fromarray(ndimg)).show()
            print(ndimg.ndim)
            # ndimg = ndimg[360:440,700:820,:] #slice to specific region I want
            (Image.fromarray(ndimg)).show()
            ndimgB, ndimgG, ndimgR = Split_channels(ndimg)
            # (Image.fromarray(ndimgB)).show()
            # (Image.fromarray(ndimgG)).show()
            # (Image.fromarray(ndimgR)).show()
            ndimg = Grayscale(ndimg)
            (Image.fromarray(ndimg)).show()
            # ndimg = Average(ndimg)
            # (Image.fromarray(ndimg)).show()
Process()