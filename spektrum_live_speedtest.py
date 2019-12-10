from matplotlib import pyplot as plt
from matplotlib import mlab as mlab
import matplotlib.animation as animation
from rtlsdr import RtlSdr
#import numpy as np
import time


sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.4e6  # min is 1e6 // max is 3.2e6 // std is 2.4e6 (Hz)
sdr.center_freq = 94.7e6  # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

fig = plt.figure()
graph_out = fig.add_subplot(1, 1, 1)

speed_num = 0
speed_sampling = 0
speed_fft = 0
speed_plot = 0


def animate(i):
    global speed_num
    global speed_sampling
    global speed_fft
    global speed_plot
    graph_out.clear()
    #samples = sdr.read_samples(256*1024)
    t1 = time.time()
    samples = sdr.read_samples(8*1024)
    t2 = time.time()
    # use matplotlib to estimate and plot the PSD
    power, psd_freq = mlab.psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                               1e6)
    psd_freq = psd_freq + sdr.center_freq/1e6
    t3 = time.time()
    graph_out.semilogy(psd_freq, power)
    t4 = time.time()
    speed_num += 1
    speed_sampling += (t2-t1)
    speed_fft += (t3-t2)
    speed_plot += (t4-t3)
    #graph_out.xlabel('Frequency (MHz)')
    #graph_out.ylabel('Relative power (dB)')


try:
    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.show()
    print(f"Timings (over {speed_num} cycles):\nSampling: {speed_sampling/speed_num*1000}\nMath: {speed_fft/speed_num*1000}\nPlotting: {speed_plot/speed_num*1000}")
except KeyboardInterrupt:
    pass
finally:
    sdr.close()
