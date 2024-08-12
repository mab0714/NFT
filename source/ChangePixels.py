from PIL import Image
import random

# Import an image from directory:
input_image = Image.open("C:\\Users\\Marvin\\Desktop\\NFT\\Cartoon_Puppy.png")
  
# Extracting pixel map:
pixel_map = input_image.load()
  
# Extracting the width and height 
# of the image:
width, height = input_image.size
 
known_colors = {}

# taking half of the width:
for i in range(width):
	for j in range(height):
		# getting the RGB pixel value.
		r, g, b = input_image.getpixel((i, j))
		
		if str(r) + "_" + str(g) + "_" + str(b) in known_colors:
			(r,g,b) = known_colors.get(str(r) + "_" + str(g) + "_" + str(b))
		else:
			delta = 255
			newR = random.randint(max(r-delta,0),min(r+delta,255))
			newG = random.randint(max(g-delta,0),min(g+delta,255))
			newB = random.randint(max(b-delta,0),min(b+delta,255))
			known_colors[str(r) + "_" + str(g) + "_" + str(b)] = (newR,newG,newB)
			
		# setting the pixel value.
		pixel_map[i, j] = (int(r),int(g),int(b))
  
# Saving the final output
# as "1.png":
#input_image.save("1.png", format="png")
  
# use input_image.show() to see the image on the
# output screen.
input_image.show()