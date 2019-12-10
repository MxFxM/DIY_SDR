from matplotlib import pyplot as plt
from matplotlib import mlab as mlab
import matplotlib.animation as animation

from rtlsdr import RtlSdr

import numpy as np
import math

from PIL import Image

sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 94.7e6  # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

fig = plt.figure()
graph_out = fig.add_subplot(1, 1, 1)

image = []


def animate(i):
    graph_out.clear()
    # samples = sdr.read_samples(256*1024)
    samples = sdr.read_samples(16*1024)
    # use matplotlib to estimate and plot the PSD
    power, psd_freq = mlab.psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                               1e6)
    psd_freq = psd_freq + sdr.center_freq/1e6
    graph_out.semilogy(psd_freq, power)
    image.append(power)


def mymap(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


try:
    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.show()

    max_pow = 0
    min_pow = 10
    largearray = np.zeros((1024), np.ubyte)[np.newaxis]
    largearray = np.transpose(largearray)
    for arr in image:
        for dat in arr:
            #dat = 10 * math.log10(dat)
            if dat > max_pow:
                max_pow = dat
            elif dat < min_pow:
                min_pow = dat

    imagelist = []
    for arr in image:
        thislist = []
        for dat in arr:
            #dat = 10 * math.log10(dat)
            thislist.append(mymap(dat, min_pow, max_pow, 0, 255))
        imagelist.append(thislist)
        #thisarray = np.array(thislist)[np.newaxis]
        #thisarray = np.transpose(thisarray)
        # print(thisarray.shape)
        # print(thisarray)
        # print(largearray)
        #largearray = np.concatenate((largearray, thisarray))
    largearray = np.array(imagelist, np.ubyte)

    im = Image.fromarray(largearray, mode='L')
    im.save("ichbineinwasserfall.jpg")
    im.save("ichbineinwasserfall.bmp")

    # print(f"{imagelist[0]}")
    # print(f"max is {max_pow} and min is {min_pow}")


except KeyboardInterrupt:
    pass
finally:
    sdr.close()
