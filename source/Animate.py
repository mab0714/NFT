from PIL import Image

im = Image.open('output\\Celebrity\\Athletes\\Basketball\\KobeBryant\\KobeBryantNoMaskWiki.png')
im.putalpha(255)
width, height = im.size
pixels = im.load()

def fade_image(image, p1, p2, flow_up=False):
    fade_range = list(range(int(height*p1), int(height*p2)))
    fade_range = fade_range[::-1] if flow_up else fade_range
    for y in fade_range:
        if flow_up:
            alpha = int((y - height*p1)/height/(p2-p1) * 255)
        else:
            alpha = 255-int((y - height*p1)/height/(p2-p1) * 255)
        for x in range(width):
            pixels[x, y] = pixels[x, y][:3] + (alpha,)

fade_image(pixels, 0.1, 1. , flow_up=False)
fade_image(pixels, 0, 0.1, flow_up=True)
im.save('output\\KobeBryantNoMaskWikiAnimated.gif')

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from wordcloud import wordcloud, ImageColorGenerator

"""
from itertools import count
from random import random

from matplotlib import pyplot as plt

import animation

x=[]
y=[]
i = count()
def animate(j):
    x.append(next(i))
    y.append(random.randint(0, 10))
    plt.plot(x,y)

animation_1 = animation.FuncAnimation(plt.gcf(),animate,interval=1000)
plt.show()

"""
"""
#image_colors = ImageColorGenerator('output\\GunViolenceInSchoolNoMask_File_Final.png')

f = plt.figure(figsize=(50, 50))
plt.plot(1, 1)
im = plt.imshow(wordcloud)


def update(i):
    A = np.random.randn(10, 10)
    im.set_array(A)
    return im


# plt.title('Art', size=80)
plt.axis("off")
plt.savefig('output\\animate.png')

ani = FuncAnimation(plt.gcf(), update, frames=range(100), interval=5, blit=False)
ani.save('output\\animate.gif', writer='imagemagick')

plt.show()
"""