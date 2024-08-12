import glob

from PIL import Image


def make_gif(images, startindex, endindex, gifnumber):
    gifImages = []
    for i in range(startindex,endindex):
        gifImages.append(Image.open(images[i]))

    gifImageOne = gifImages[0]

    gifImageOne.save("C:\\Users\\Marvin\\Desktop\\NFT\\Personal\\Jameson_Puppy\\gifs\\Jameson"+str(gifnumber)+".gif", format="GIF", append_images=gifImages, save_all=True, duration=5, loop=0)

    #frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.PNG")]

    #frame_one = frames[0]
    #frame_one.save("my_awesome.gif", format="GIF", append_images=frames, save_all=True, duration=100, loop=0)


if __name__ == "__main__":
    frame_folder = "C:\\Users\\Marvin\\Desktop\\NFT\\Personal\\Jameson_Puppy\\build\\images"
    images = glob.glob(f"{frame_folder}/*.PNG")
    count = len(images)
    increment = int(count/10) #count

    startindex = 1
    endindex = increment
    gifcounter = 1
    while (endindex <= count):
        make_gif(images, startindex, endindex,gifcounter)
        startindex += increment
        endindex += increment
        gifcounter += 1
