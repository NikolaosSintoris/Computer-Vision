import numpy as np
from PIL import Image
import os
import sys
  
def convert_rgb_to_grayScale(image, image_shape):
	new_image = np.zeros((image_shape[0], image_shape[1]))
	for i in range(0, image_shape[0]):
		for j in range(0, image_shape[1]):
			new_image[i][j] = np.average(image[i][j])
	return new_image  

# We know that 0 is black and 255 is white.
# According to this, we understand that the text is the pixels with small values, 
# and the background is the pixels with large values.
# So, every value that is lower than my threshold i will set it to 0 (black).
def thresholding(image, threshold):
    new_image = np.copy(image) 
    image_shape = new_image.shape
    for i in range(0, image_shape[0]):
        for j in range(0, image_shape[1]):
            if(new_image[i, j] < threshold):
                new_image[i, j] = 0
            else:
                new_image[i, j] = 255         
    return new_image


currentDirectory = os.getcwd() # Save the current working directory.
input_filename = sys.argv[1] # Take the input filename.
output_filename = sys.argv[2] # Take the output filename.
threshold = int(sys.argv[3]) # Take the threshold.
image = np.array(Image.open(currentDirectory + "/" + input_filename)) # Opens the image from my hard drive.
image_shape = image.shape # The shape of the image.
# Check if image is rgb. 
#If it is, then convert it to grayscale according to the rule "mean value of RED, GREEN, BLUE canals".                           
if(len(image_shape) == 3):
	image = convert_rgb_to_grayScale(image, image_shape)
print("Before thresholding")
print("The array is the following: ")
print(image)

new_image = np.zeros((image.shape[0], image.shape[1])) # Initialize an array.
print("\nAfter thresholding")
print("The array is the following: ")
new_image = thresholding(image, threshold)
print(new_image)

Image.fromarray(np.uint8(new_image)).save(currentDirectory + "/" + output_filename) # Save the image to the current working directory.