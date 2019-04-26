from PIL import Image
import glob
import os
import pyqtgraph as pg
import easygui
import numpy as np

uin = str
data = []
datasets = []
name = []
names = []

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
    imagebool = True
    path = easygui.diropenbox()
    try:
        images = glob.glob(path + '/*.jpg') #Get full path of images in folder
    except:
        Menu()
    print("Working...")
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
            if imagebool == True:
                (Image.fromarray(ndimg)).show()
                imagebool = False

        timestamps.append(image.rsplit("_", 1))
    for extra in timestamps:
        del(extra[0])
    timestamps = Flatten(timestamps)
    for time in timestamps:
        time = time[0:-4]
    
    # print(timestamps)
    # print(average_values)
    print("Added dataset " + path)
    return(average_values, path)

def Plot(datasets, names):
    plotWidget = pg.plot(title="Plotted values of pixel intensity")
    plotWidget.addLegend()
    for index, (dataset, name) in enumerate(zip(datasets, names)):
        plotWidget.plot(dataset, pen = (index), name = name)

def Menu():
    global data 
    global datasets
    global name
    global names
    uin = input("""

What would you like to do?
1. Add datapoints from images
2. Finish graph and visualize
3. Quit
""")
    if uin == "1":
        data, name = Process()
        datasets.append(data)
        names.append(name)
        Menu()
    elif uin == "2":
        if datasets:
            Plot(datasets, names)
            Menu()
        else:
            print("You have not loaded any images, or loaded images incorrectly.")
            Menu()
    elif uin == "3":
        uin = input("Really quit? (y/n): ")
        if uin == "y" or "Y" or "Yes" or "yes":
            exit()
        else:
            Menu()
    else:
        Menu()

print("""

Welcome to the Flow Cell Project Image Processing Script!""")
Menu()




