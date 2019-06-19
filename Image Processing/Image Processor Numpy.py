# This script is intended to be used after having created a dataset of images of the flow cell using the server.py video capture feature and the flow cell imaging platform. 
from PIL import Image
import glob
import os
import pyqtgraph as pg
import easygui
import numpy as np
import cv2
uin = str
data = []
datasets = []
name = []
names = []

# Exporting image using PyQTGraph interactive window not working? This is a possible cause and fix: https://groups.google.com/forum/?nomobile=true#!topic/pyqtgraph/4jiAPUpLpF4

def Linreg():
    for idx, (dataset, name) in enumerate(zip(datasets, names)):
        x = np.arange(0, len(dataset))
        y = np.array(dataset)
        z = np.polyfit(x,y,1)
        print("First degree linear regression of dataset " + name + " is: " + "{0}x + {1}".format(*z))
        
def Normalize(values): # Normalizes an input list of values to floats in a range 0 to 1. Returns a list of the same length with the rescaled values
    valmin = min(values)
    valmax = max(values)
    for i, val in enumerate(values):
        values[i] = (val-valmin) / (valmax - valmin)
    return values

def Average(array): # Returns the average value of an array of values.
    return np.mean(array)

def Flatten(list_of_lists): # 'Flattens' nested lists. Returns one big list with the contents of all lists in list_of_lists.
    flattened_list = []
    for lst in list_of_lists:
        for item in lst:
            flattened_list.append(item)
    return flattened_list 

def Grayscale(imgarray, weights = np.c_[0.2989, 0.5870, 0.1140]): # 
    tile = np.tile(weights, reps=(imgarray.shape[0], imgarray.shape[1], 1)) #create a new array that is the same size as image array. new array consists of multipliers for every pixel according to the weights given.
    return np.sum(tile * imgarray, 2) #multiply pixel values in image array with weights from newly created array

def Split_channels(imgarray): # Split an image into separate blue, green, red color channels.
    imgB = imgarray[:,:,0]
    imgG = imgarray[:,:,1]
    imgR = imgarray[:,:,2]
    return imgB, imgG, imgR

def Process():
    path = easygui.diropenbox()
    try:
        images = glob.glob(path + '/*.jpg') #Get full path of images in folder
    except:
        print("Not a valid path.")
        Menu()
    average_values = []
    timestamps = []
    with open((sorted(images)[-1]), 'rb') as file:
        imgfull = Image.open(file)
        ndimg = np.array(imgfull)
        r_channel = cv2.selectROI("Select a region of image to use as channel region.", ndimg)
        cv2.destroyAllWindows()
        r_normal = cv2.selectROI("Select a region to use as normalisation region.",ndimg)
        cv2.destroyAllWindows()
    print("Working...")

    for image in sorted(images): # For each image in sorted folder of images, open and convert to NumPy ndarray. User specifies region to analyze, as well as region to use as normalization region. The average value of a frame's region of interest is calculated as the difference between the 
        with open(image, 'rb') as file:
            imgfull = Image.open(file)
            ndimg = np.array(imgfull) #open as ndarray
            normalregion = ndimg[int(r_normal[1]):int(r_normal[1]+r_normal[3]), int(r_normal[0]):int(r_normal[0]+r_normal[2])] # Slice to region specified by previously set normal ROI box
            ndimg = ndimg[int(r_channel[1]):int(r_channel[1]+r_channel[3]), int(r_channel[0]):int(r_channel[0]+r_channel[2])] # Slice to region specified by previously set channel ROI box
            normalregion = Grayscale(normalregion)
            ndimg = Grayscale(ndimg)
            normal_average = Average(normalregion)
            channel_average = Average(ndimg)
            average_values.append(channel_average - normal_average)

        timestamps.append(image.rsplit("_", 1)) #Clean up timestamps 
    for extra in timestamps:
        del(extra[0])
    timestamps = Flatten(timestamps)
    for time in timestamps:
        time = time[0:-4]
    average_values = Normalize(average_values)
    print("Added dataset " + path)
    return(average_values, path)

def Plot(datasets, names):
    plotWidget = pg.plot(title="Plotted values of pixel intensity")
    plotWidget.addLegend()
    for index, (dataset, name) in enumerate(zip(datasets, names)):
        plotWidget.plot(dataset, pen = (index), name = "Dataset ID: " + str(index) + ". Path: " + name)

def Menu():
    global data 
    global datasets
    global name
    global names
    uin = input("""

What would you like to do?
1. Add datapoints from images
2. Finish graph and visualize
3. Display Linear Regression of loaded datasets
4. Quit
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
        Linreg()
        Menu()
    elif uin == "4":
        uin = input("Really quit? (y/n): ")
        if uin == "y" or "Y" or "Yes" or "yes":
            exit()
        else:
            Menu()
    else:
        print("Invalid entry.")
        Menu()

print("""

Welcome to the Flow Cell Project Image Processing Script!""")
Menu()