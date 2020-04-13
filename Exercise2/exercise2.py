import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import distance
import os
import sys


currentDirectory = os.getcwd() # Save the current working directory
input_filename = sys.argv[1] # Take the input filename
output_filename = sys.argv[2] # Take the output filename

# Take the transformation matrix elements.
a1 = float(sys.argv[3])
a2 = float(sys.argv[4])
a3 = float(sys.argv[5])
a4 = float(sys.argv[6])
a5 = float(sys.argv[7])
a6 = float(sys.argv[8])

image = np.array(Image.open(currentDirectory + "/" + input_filename)) # Opens the image from my hard drive.
image_shape = image.shape
# I create a matrix with size: (3, 101*101) that has the coordinates of the original image.
# I want the middle pixel of the image, as the beginning of the axes.
previous_coordinates = np.zeros( [3, image_shape[0]*image_shape[1]] )
previous_coordinates[2, :] = 1 
for i in range(image_shape[0]):
	for j in range(image_shape[1]):
		pos = i*101 + j
		previous_coordinates[0, pos] = i - 50
		previous_coordinates[1, pos] = j - 50
previous_coordinates = previous_coordinates.astype(int)        

# This is my transformation matrix.
transform_matrix = np.array([ 	[a1, a2, a3],
								[a4, a5, a6],
                              	[0, 0, 1] 
							])
after_transformation_matrix = transform_matrix @ previous_coordinates # @: matrix multiplication.

# I need to move again my matrix to have my final coordinates.
# So, the matrix final_coordinates has my final coordinates.
# I store, only the valid final coordinates in a list with a name valid_coordinates, so i do not need to do unnecessary comparisons.
# I check my results and i did not have a problem.
valid_coordinates = []
final_coordinates = np.zeros( [3, image_shape[0]*image_shape[1]] )
final_coordinates[2, :] = 1 
for i in range(image_shape[0]):
	for j in range(image_shape[1]):
		pos = i*101 + j
		coordinate_x = after_transformation_matrix[0, pos] + 50
		coordinate_y = after_transformation_matrix[1, pos] + 50
		final_coordinates[0, pos] = coordinate_x
		final_coordinates[1, pos] = coordinate_y
		if((0 <= coordinate_x < image_shape[0]) and (0 <= coordinate_y < image_shape[1])):
			valid_coordinates.append([coordinate_x, coordinate_y, i, j])

# I want to fill all the pixels of the new image, with their closest neighbourhood intensity.
new_image = np.full([image_shape[0], image_shape[1]], 0, dtype = int)
for final_i in range(image_shape[0]):
	print("Line: ", final_i)# I let this print, so that i know when my program will end.
	for final_j in range(image_shape[1]):
		min_i = 0
		min_j = 0
		min_euclidean_distance = 2000
		for i in range(len(valid_coordinates)):
			d = distance.euclidean((final_i, final_j), (valid_coordinates[i][0], valid_coordinates[i][1]))
			if(d <= min_euclidean_distance):
				min_euclidean_distance = d
				min_i = valid_coordinates[i][2]
				min_j = valid_coordinates[i][3]
		new_image[final_i, final_j] = image[min_i, min_j]
Image.fromarray(np.uint8(new_image)).save(currentDirectory + "/" + output_filename)		
print("\nProgram terminated succesfully!")        