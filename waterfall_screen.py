"""
Gets live data from Nooelec SDR and
displays a waterfall accordingly.
Center Frequency is 94.7MHz.
"""

from matplotlib import mlab
from rtlsdr import RtlSdr
import numpy as np
from PIL import Image
import pygame

DISPLAY_WIDTH = 256
DISPLAY_HEIGHT = 200

SDR = RtlSdr()
# configure device
SDR.sample_rate = 2.4e6  # Hz
SDR.center_freq = 94.7e6  # Hz
SDR.freq_correction = 60   # PPM
SDR.gain = 'auto'


IMAGE = []


def get_data():
    """
    Reads new samples and updates output image.
    """

    samples = SDR.read_samples(16*1024)
    power, _ = mlab.psd(samples, NFFT=1024, Fs=SDR.sample_rate /
                        1e6)

    max_pow = 0
    min_pow = 10

    # search whole data set for maximum and minimum value
    for dat in power:
        if dat > max_pow:
            max_pow = dat
        elif dat < min_pow:
            min_pow = dat

    # update image data
    imagelist = []
    for dat in power:
        imagelist.append(mymap(dat, min_pow, max_pow, 0, 255))
    IMAGE.append(imagelist[round(len(
        imagelist)/2)-round(len(imagelist)/8): round(len(imagelist)/2)+round(len(imagelist)/8)])
    if len(IMAGE) > 200:
        IMAGE.pop(0)


def mymap(val, in_min, in_max, out_min, out_max):
    """
    Returns the value which was mapped between in_min and in_max,
    but now mapped between out_min and out_max.
    If value is outside of bounds, it will still be outside afterwards.
    """

    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


pygame.init()
GAMEDISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(f"DIY SDR")
CLOCK = pygame.time.Clock()
BACKGROUND = pygame.Surface(GAMEDISPLAY.get_size())
BACKGROUND = BACKGROUND.convert()
BACKGROUND.fill((0, 0, 0))

GAMEQUIT = False

while not GAMEQUIT:

    GAMEDISPLAY.blit(BACKGROUND, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEQUIT = True

    get_data()
    OUTIMAGE = np.array(IMAGE, np.ubyte)
    OUTIMAGE = Image.fromarray(OUTIMAGE, mode='L')
    OUTIMAGE = OUTIMAGE.convert('RGBA')
    RAWSTR = OUTIMAGE.tobytes("raw", 'RGBA')
    SURFACE = pygame.image.fromstring(RAWSTR, OUTIMAGE.size, 'RGBA')
    GAMEDISPLAY.blit(SURFACE, (0, 0))
    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()
SDR.close()