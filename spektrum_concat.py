from rtlsdr import RtlSdr
import matplotlib.pyplot as plt
from matplotlib import mlab as mlab
import numpy as np

powe = np.ndarray(0)
freq = np.ndarray(0)

SAMPLERATE = 2.4e6  # Hz

for i in np.arange(50, 1000, SAMPLERATE/1e6):
    sdr = RtlSdr()

    # configure device
    sdr.sample_rate = SAMPLERATE
    sdr.center_freq = i*1e6  # Hz
    sdr.freq_correction = 60   # PPM
    sdr.gain = 'auto'  # 4
    samples = sdr.read_samples(8*1024)
    sdr.close()
    sdr = None
    # use matplotlib to estimate and plot the PSD
    power, psd_freq = mlab.psd(samples, NFFT=1024, Fs=SAMPLERATE /
                               1e6)
    psd_freq = psd_freq + i
    powe = np.concatenate((powe, np.array(power)))
    freq = np.concatenate((freq, np.array(psd_freq)))
    print(f"{i}/1000")

plt.semilogy(freq, powe)

plt.xlabel('Frequency (MHz)')
plt.ylabel('Relative power (dB)')
plt.show()
