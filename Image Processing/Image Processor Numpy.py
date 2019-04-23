from PIL import Image
import glob
import pyqtgraph as pg
import numpy as np
uin = str
images = glob.glob(input('Please enter full path to folder containing captured images: ') + '/*.jpg') #Get full path of images in folder

def Average(array):
    return np.mean(array) #dimensions should be tuple of axis to average

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
    average_values = []
    timestamps = []
    for image in sorted(images):
        with open(image, 'rb') as file:
            imgfull = Image.open(file)
            ndimg = np.array(imgfull) #open as ndarray
            ndimg = ndimg[250:300,235:290,:] #slice to specific region I want
            # ndimgB, ndimgG, ndimgR = Split_channels(ndimg)
            average_values.append(Average(ndimg))
            ndimg = Grayscale(ndimg)
        timestamps.append(image.rsplit("_", 1))
    for extra in timestamps:
        del(extra[0])
    timestamps = Flatten(timestamps)
    for time in timestamps:
        time = time[0:-4]
    print(timestamps)
    print(average_values)
    (Image.fromarray(ndimg)).show()
    pg.plot(average_values, symbol = None)
Process()
