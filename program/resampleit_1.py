import numpy as np
import scipy.signal as sig
import scipy.interpolate as interp
import PyGnuplot as gp
import math

n = 2048 # number of samples
f0 = 1000 # first frequency
fdot = 16000 # output frequency

time = np.arange(2048)
signal = np.zeros(2048)
for i in range(1, fdot // (2 * f0)):
    signal += np.sin(2 * np.pi * time * i * f0 / fdot) / (i**2)

x_16 = signal
f_16 = np.fft.rfftfreq(2048, 1 / 16000)
sp_16 = 20 * np.log10(np.abs(np.fft.rfft(x_16 * np.hamming(2048))) /1024)
#gp.c('')
#gp.figure(1)
#gp.s([f_16, sp_16])
#gp.c('set title "Widmo sygnału testowego"')
#gp.c('set xlabel "Częstotliwość [Hz]"')
#gp.c('set ylabel "Amplituda [dB]"')
#gp.c('set grid')
#gp.c('unset key')
#gp.c('plot "tmp.dat" lc rgb "#8b1a0e" w l')

# Interpolacja do x_48
x_48 = np.zeros(2048 * 3)
x_48[1::3] = x_16
f_48 = np.fft.rfftfreq(2048, 1 / 48000)
sp_48 = 20 * np.log10(np.abs(np.fft.rfft(x_48[:2048] * np.hamming(2048))) / 1024)
gp.s([f_48, sp_48],'tmp1.dat')
gp.c('set title "Widmo sygnału testowego"')
gp.c('set xlabel "Częstotliwość [Hz]"')
gp.c('set ylabel "Amplituda [dB]"')
gp.c('set grid')
gp.c('unset key')
gp.c('plot "tmp1.dat" lc rgb "#8b1a0e" w l')
