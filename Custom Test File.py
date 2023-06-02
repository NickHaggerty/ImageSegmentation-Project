#Import your class (it should be in same directly as this file)
import segmentationClass
from PIL import Image

#IMport numpy, and plotting package
import numpy as np
from matplotlib import pyplot as plt

#Filed image to be segmented. Top left is background, bottom right is foreground. 
ImageFile = "Nature.png"

#Instantiate an object for your class. 
obj = segmentationClass.segmentationClass()
print("Image processing...\n\nThis may take a minute or two.")

#import the image and set it to a np.array
img = Image.open(ImageFile).resize((30,30))
img = np.array(img)

#set background and foreground
obj.x_a = np.array([29,29]);  # Foreground pixel coordinate
obj.x_b = np.array([0,0]);  # Background pixel coordinate
obj.p0 = 1; 
#segment the image
segImage = obj.segmentImage(img);

#Create plot
fig, axs = plt.subplots(1,2)



#make original plot
axs[0].set_title("Input image")
axs[0].imshow(img)

#make segmented plot
axs[1].set_title("Segmented Image")
axs[1].imshow(255*segImage.astype(np.uint8), interpolation='nearest')

#show results
plt.show()
