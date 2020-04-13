Info about exercise1.      
Compile program: python3 exercise1.py input_filename output_filename  threshold

I implemented an image editing program, that executes vertical image input.   
After loading the manuscript, i edited it to create distorted images (This process is called thresholding).    
Limitation is a way of creating binary images, that is, images that have in each pixel one of only two possible intensity values.    
Our goal in the demarcated image is for the white color to correspond to the background, and the color to correspond to the areas of interest of the image, which in our case is the text itself.   
The code is working whether the user's image is grayscale (like the handwriting given) or the image is RGB.   
If the input image is RGB, i convert it to grayscale by simply taking the average of the Red, Green, Blue channels.

To test the code, i uploaded trikoupi6.png, which is a grayscale image.
