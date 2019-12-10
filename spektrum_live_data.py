from matplotlib import pyplot as plt
from matplotlib import mlab as mlab
import matplotlib.animation as animation
from rtlsdr import RtlSdr

sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 94.7e6  # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

fig = plt.figure()
graph_out = fig.add_subplot(1, 1, 1)


def animate(i):
    graph_out.clear()
    samples = sdr.read_samples(16*1024)
    power, psd_freq = mlab.psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                               1e6)
    psd_freq = psd_freq + sdr.center_freq/1e6
    graph_out.semilogy(psd_freq, power)


try:
    ani = animation.FuncAnimation(fig, animate, interval=10)
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    sdr.close()
