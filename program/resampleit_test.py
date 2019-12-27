import numpy as np
import scipy.signal as sig
import scipy.interpolate as interp
import PyGnuplot as gp
gp.default_term = 'wxt'
import math
import wfdb
from wfdb import processing
import ipdb

def plot(x, y, figure, title="Title", xlabel="xlabel", xunit="xunit", ylabel='ylabel', yunit="yunit"):
    gp.figure(figure)
    filename = 'tmp_plot' + str(figure) + '.dat'
    gp.s([x, y], filename)
    gp.c('set title "' + title + '"')
    gp.c('set xlabel "' + xlabel + ' [' + xunit + ']"')
    gp.c('set ylabel "' + ylabel + ' [' + yunit + ']"')
    gp.c('set grid')
    gp.c('unset key')
    gp.c('plot "' + filename + '" lc rgb "#8b1a0e" w l')
#end of plot(x, y, figure, ...

""" ======================================================================== """

# reading MIT file
record = wfdb.rdsamp('./data/ansiaami-ec13-test-waveforms-1.0.0/aami3a')
# create time vector
time = np.linspace(0, record[1]['sig_len']/record[1]['fs'], record[1]['sig_len'])
# create signal vector
signal = np.concatenate(record[0])
# plot it
plot(time, signal, 1, 'Signal before resampling', ylabel="Amplituda", yunit="mV", xlabel="Czas", xunit="s")

""" current work """
#record1 = wfdb.rdrecord('./data/ansiaami-ec13-test-waveforms-1.0.0/aami3a')
#wfdb.plot_wfdb(record=record1, title='title')

# spectrum calculation
fft = np.fft.fft(signal)
freq = np.fft.fftfreq(len(signal), 1/720)

signal_200 = processing.resample_sig(signal, 720, 200)
time_200 = np.linspace(0, len(signal_200[0])/200, len(signal_200[0]))
plot(time_200, signal_200[0], 4, title='Signal ECG after resampling')

fft_200 = np.fft.fft(signal_200[0])
freq_200 = np.fft.fftfreq(len(signal_200[0]), 1/200)

plot(freq, np.abs(fft), 5, title='Spectrum '.join(record[1]['sig_name']), ylabel="Amplituda", yunit="dB", xlabel="Częstotliwość", xunit="Hz")
plot(freq_200, np.abs(fft_200), 6, title='Spectrum '.join(record[1]['sig_name']), ylabel="Amplituda", yunit="dB", xlabel="Częstotliwość", xunit="Hz")

ipdb.set_trace()
