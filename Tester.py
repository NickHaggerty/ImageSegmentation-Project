# Author: Jordan Malof
# Date: 2022.12.07
# Version: 2
#Import your class (it should be in same directly as this file)
import segmentationClass
#IMport numpy, and plotting package
import numpy as np
from matplotlib import pyplot as plt
#Instantiate an object for your class.
obj = segmentationClass.segmentationClass()
## Create a simple test image
# The image has two red pixels, and other pixels are zero-valued
I = np.zeros([3,3,3]);
I[2,2,0]=128;
I[1,2,0]=128;
#Set segmentation object properties
obj.x_a = np.array([0,0]); # Foreground pixel coordinate
obj.x_b = np.array([2,2]); # Background pixel coordinate
obj.p0 = 1; # Edge capacities between neighboring pixels
# Segment the image
# This method and its I/O are needed in your implementaiton
t = obj.segmentImage(I);
# Plot the results
fig, axs = plt.subplots(1,2)
fig.suptitle('Input and segmentation')
axs[0].imshow(I.astype(np.uint8), interpolation='nearest')
axs[0].set_title("Input image (3x3)")
# The matrix 't' is binary, but it is helpful to scale the values to be 0 or 255
# when displaying with imshow
axs[1].imshow(255*t.astype(np.uint8), interpolation='nearest')
axs[1].set_title("Binary segmentation")
plt.show()
