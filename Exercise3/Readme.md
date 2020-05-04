  I implemented an adaptive threshold algorithm, extending the basic Otsu method. This means that there will be no threshold for the whole image, but a different threshold for each individual icon. For each pixel I take the pixels around a neighborhood (that is, as if they were the whole image at a time), and calculate a threshold by maximizing its objective function Otsu. Where the window of the neighborhood 'goes out' of the boundaries of the image, I ignore those pixels.
  
  The code works whether the user image is grayscale or the image is colored. If the input image is colored, it is converted to grayscale by simply taking the average of the Red, Green, Blue channels.

  To test the code, I uploaded trikoupi6_low.png, which is a grayscale image.
