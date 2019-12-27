import numpy as np
import scipy.signal as sig
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import math

def generuj_sygnal(n, f0, fs):
    '''Generuje n próbek sygnału złożonego z sinusów, o częstotliwości pierwszego sinusa równej f0,
    przy częstotliwości próbkowania fs.
    '''
    t = np.arange(n)
    sygnal = np.zeros(n)
    for i in range(1, fs // (2 * f0)):
        sygnal += np.sin(2 * np.pi * t * i * f0 / fs) / (i**2)
    return sygnal

x_16 = generuj_sygnal(2048, 1000, 16000)
f_16 = np.fft.rfftfreq(2048, 1 / 16000)
sp_16 = 20 * np.log10(np.abs(np.fft.rfft(x_16 * np.hamming(2048))) /1024)
plt.plot(f_16, sp_16)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda [dB]')
plt.title('Widmo sygnału testowego')
plt.show()

x_48 = np.zeros(2048 * 3)
x_48[1::3] = 3 * x_16
f_48 = np.fft.rfftfreq(2048, 1 / 48000)
sp_48 = 20 * np.log10(np.abs(np.fft.rfft(x_48[:2048] * np.hamming(2048))) / 1024)
plt.plot(f_48, sp_48)
plt.xlabel('częstotliwość [Hz]')
plt.ylabel('amplituda [dB]')
plt.title('Widmo sygnału po wstawieniu zer')
plt.show()

print(sig.firwin(31, 0.5))

b_up3 = sig.firwin(301, 1 / 3)
x_48 = np.zeros(2048 * 3)
x_48[1::3] = x_16
x_48 = 3 * sig.filtfilt(b_up3, 1, x_48)
f_48 = np.fft.rfftfreq(2048, 1 / 48000)
sp_48 = 20 * np.log10(np.abs(np.fft.rfft(x_48[:2048] * np.hamming(2048))) / 1024)
plt.plot(f_48, sp_48)
plt.xlabel('częstotliwość [Hz]')
plt.ylabel('amplituda [dB]')
plt.title('Widmo sygnału po interpolacji L=3')
plt.show()

fig, ax = plt.subplots(2)
ax[0].plot(x_16[200:300], label="fs=16 kHz")
ax[1].plot(x_48[600:700], label="fs=48 kHz")
for a in ax:
    a.set_xlabel('nr próbki')
    a.set_ylabel('amplituda')
    a.legend(loc='upper right')
ax[0].set_title('Sygnał testowy przed i po interpolacji')
plt.show()

fig, ax = plt.subplots(2)
ax[0].plot(x_16[200:210], 'o-', label="fs=16 kHz")
ax[1].plot(x_48[600:630], 'o-', label="fs=48 kHz")
for a in ax:
    a.set_xlabel('nr próbki')
    a.set_ylabel('amplituda')
    a.legend()
ax[0].set_title('Sygnały przed i po interpolacji')
plt.show()

x_48 = sig.resample_poly(x_16, 3, 1)
f_48 = np.fft.rfftfreq(2048, 1 / 48000)
sp_48 = 20 * np.log10(np.abs(np.fft.rfft(x_48[:2048] * np.hamming(2048))) / 1024)
plt.plot(f_48, sp_48)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda [dB]')
plt.title('Widmo sygnału interpolowanego funkcją resample_poly')
plt.show()
