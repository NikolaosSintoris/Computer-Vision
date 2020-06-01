# python3 warp.py <input filename> <output filename>
# Nikolaos Sintoris A.M: 3071

import numpy as np 
from PIL import Image
from matplotlib import pyplot as plt
import cv2
from numpy.linalg import inv
import os
import sys

def Sort(sub_li): 
    sub_li.sort(key = lambda x: x[1]) 
    return sub_li 

currentDirectory = os.getcwd() # Save the current working directory
input_filename = sys.argv[1] # Take the input filename
output_filename = sys.argv[2] # Take the output filename
image_path = currentDirectory + "/" + input_filename


#Opens the image from the hard drive.
image = np.array(Image.open(image_path)) 

# A function that stores the point(coordinate_X, coordinate_y) when a user click(left), to a list.
user_points = []
def collect_points(event, x, y, flags, params):
    if(event == cv2.EVENT_LBUTTONDOWN):
        user_points.append([x, y])

# Creates a frame with the image so that the user can interact.    
img = cv2.imread(image_path)
cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Frame", collect_points)
while True:
    cv2.imshow("Frame", img)
    key = cv2.waitKey(1)
    if(key == 27): # Exits when esc button is pressed.
        break
cv2.destroyAllWindows()  

# b array: corner coordinates of my new image.
b = np.array([0, 0, 999, 0, 0, 999,  999, 999])

# Fix the order of the points.
# the order i want is: (upper left corner - upper right corner - bottom left corner - bottom right corner)
sort_second_element_list = Sort(user_points)
sublist1 = sort_second_element_list[0:2]
sublist2 = sort_second_element_list[2:]
sublist1.sort()
sublist2.sort()

x1 = sublist1[0][0]
y1 = sublist1[0][1]
x2 = sublist1[1][0]
y2 = sublist1[1][1]
x3 = sublist2[0][0]
y3 = sublist2[0][1]
x4 = sublist2[1][0]
y4 = sublist2[1][1]

new_x1 = b[0]
new_y1 = b[1]
new_x2 = b[2]
new_y2 = b[3]
new_x3 = b[4]
new_y3 = b[5]
new_x4 = b[6]
new_y4 = b[7]

A = np.array( [[x1, y1, 1, 0, 0, 0, -x1*new_x1, -y1*new_x1],
               [0, 0, 0, x1, y1, 1, -x1*new_y1, -y1*new_y1],
               [x2, y2, 1, 0, 0, 0, -x2*new_x2, -y2*new_x2],
               [0, 0, 0, x2, y2, 1, -x2*new_y2, -y2*new_y2],
               [x3, y3, 1, 0, 0, 0, -x3*new_x3, -y3*new_x3],
               [0, 0, 0, x3, y3, 1, -x3*new_y3, -y3*new_y3],
               [x4, y4, 1, 0, 0, 0, -x4*new_x4, -y4*new_x4],
               [0, 0, 0, x4, y4, 1, -x4*new_y4, -y4*new_y4],
              ] )

# Invert array A.
inverse_A = inv(A) 

# The elements that I need to create my perspective transformation matrix.
x = inverse_A @ b

perspective_transformation_matrix = np.array( [[x[0], x[1], x[2]],
                                               [x[3], x[4], x[5]],
                                               [x[6], x[7], 1]
                                              ] )

new_image = cv2.warpPerspective(image, perspective_transformation_matrix,(1000, 1000), flags = cv2.INTER_LINEAR)
Image.fromarray(np.uint8(new_image)).save(currentDirectory + "/" + output_filename)
print("Program ended successfully!")