# python3 adaptive.py <input filename> <output filename> <window_size>
# Nikolaos Sintoris A.M: 3071

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

def compute_value_of_otsu_object_function(sub_image, threshold):
    segment1 = sub_image[sub_image < threshold] # A 1-D array that has all the values < threshold from image.
    segment2 = sub_image[sub_image >= threshold] # A 1-D array that has all the values >= threshold from image.
    mean_value_segment1 = 0
    mean_value_segment2 = 0
    if(segment1.size != 0): # Check if segment1 is empty.
        mean_value_segment1 = np.mean(segment1)
    if(segment2.size != 0): # Check if segment2 is empty.   
        mean_value_segment2 = np.mean(segment2)
    mean_value_of_sub_image = np.mean(sub_image)
    percentage_of_segment1 = len(segment1) / (len(segment1) + len(segment2))
    percentage_of_segment2 = len(segment2) / (len(segment1) + len(segment2))
    value_of_object_function = percentage_of_segment1 * pow(mean_value_segment1 - mean_value_of_sub_image, 2) + percentage_of_segment2 * pow(mean_value_segment2 - mean_value_of_sub_image, 2)
    return value_of_object_function

# Otsu algorithm: i will find the intensity that has the max value on otsu object function, 
#                 and i will return the best threshold.
def otsu_thresholding(sub_image):
    best_value = 0
    best_threshold = 0
    for current_threshold in range(0, 256, 5):
        current_value = compute_value_of_otsu_object_function(sub_image, current_threshold)
        if(current_value > best_value):
            best_value = current_value
            best_threshold = current_threshold 
    return best_threshold

# Create a list that has only the valid coordinates.
def valid_indexes_for_rows(old_list):
    new_list = []
    for i in old_list:
        if((i >= 0) and (i < image_shape[0])):
            new_list.append(i)
    return new_list  

def valid_indexes_for_columns(old_list):
    new_list = []
    for i in old_list:
        if((i >= 0) and (i < image_shape[1])):
            new_list.append(i)
    return new_list  

# Check if window size is even or odd number.
def check_window_size(window_size):
    if((window_size % 2) == 0):
        return True
    return False


currentDirectory = os.getcwd() # Save the current working directory
input_filename = sys.argv[1] # Take the input filename
output_filename = sys.argv[2] # Take the output filename
window_size = int(sys.argv[3]) # Take the window size
image_path = currentDirectory + "/" + input_filename

image = np.array(Image.open(image_path)) #Opens the image from the hard drive.
image_shape = image.shape # The shape of the image.

# Check if image is rgb. 
#If it is, then convert it to grayscale according to the rule "mean value of RED, GREEN, BLUE canals".                           
if(len(image_shape) == 3):
    image = convert_rgb_to_grayScale(image, image_shape)

index = int(window_size / 2)
is_window_size_even = check_window_size(window_size)

adaptive_otsu_image = np.copy(image) # The new image after adaptive otsu thresholding.
for i in range(0, image_shape[0]):
    row_list = []
    start_row_index = i - index
    if(is_window_size_even == True):
        end_row_index = i + index + 2
    else:
        end_row_index = i + index + 1
    for k in range(start_row_index, end_row_index):
        row_list.append(k)
    row_list = valid_indexes_for_rows(row_list) 
    for j in range(0, image_shape[1]):    
        column_list = []  
        start_column_index = j - index
        if(is_window_size_even == True):
            end_column_index = j + index + 2
        else:
            end_column_index = j + index + 1
        for m in range(start_column_index, end_column_index):
            column_list.append(m)
        column_list = valid_indexes_for_columns(column_list)
        sub_image = image[row_list[0]:row_list[-1]+1, column_list[0]:column_list[-1]+1]
        threshold = otsu_thresholding(sub_image)
        if(adaptive_otsu_image[i, j] < threshold):
            adaptive_otsu_image[i, j] = 0
        else:
            adaptive_otsu_image[i, j] = 255

Image.fromarray(np.uint8(adaptive_otsu_image)).save(currentDirectory + "/" + output_filename)
print("Program ended successfully!")