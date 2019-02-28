from PIL import Image
import glob
import pyqtgraph as pg

images = glob.glob('./images/Selected_Frames/*.jpg') #Get full path of image folder
print(images)

def Average(llst):
    return sum(llst) / len(llst)

def Flatten(list_of_lists):
    flattened_list = []
    for lst in list_of_lists:
        for item in lst:
            flattened_list.append(item)
    return flattened_list 

averages = []
frames = [500,1000,1500,2000, 2500, 3000, 3500, 4000]

for image in sorted(images):
    print(image)
    with open(image, 'rb') as file:
        imgfull = Image.open(file)#.convert('L') #Converts to grayscale, not needed here since I only pick the red channel later on
        img, green, blue = imgfull.split() #split image data into three arrays of pixel values
        width, height = img.size #get dimensions of image
        print("Width and Height of image is: " + str(width) + " " + str(height) + "\n")
        channelarea = tuple(((width*0.55), (height*0.525), (width*0.65), (height*0.625))) #get area to crop from dimensions of image
        print("Coordinates of crop area is: " + str(channelarea) + "\n")
        imgcenter = img.crop(channelarea)

        imgcenter.show()

        grayname = str(imgcenter)[:-4] + "gray.jpg"
        imgcenter.save(grayname)
        
        pixels = list(imgcenter.getdata())
        width, height = imgcenter.size
        pixels = [pixels[i*width:(i+1) * width]for i in range(height)]
        #print("List of pixel values: " + str(pixels) + "\n")
        #print("Flattened list of pixels: " + str(Flatten(pixels))+ "\n")
        print("Average of flattened list of pixels: " + str(Average(Flatten((pixels)))))
        averages.append(Average(Flatten((pixels))))
    print("--------------------")
print(averages)
print(frames)

pg.plot(frames,averages, symbol = 'o')


#import image
#convert to grayscale
#crop to center
# #average color value?

