import numpy as np
import scipy.signal as sig
import wfdb
from wfdb import processing
from zenipy import file_selection
import ipdb
# arguments
frequency = 1440
file_name = file_selection(multiple=False, directory=False, save=False, confirm_overwrite=False, filename=None, title='', width=330, height=120, timeout=None)
import PyGnuplot as gp
gp.default_term = 'wxt'
def plot(x, y, figure, title="Title", xlabel="xlabel", xunit="xunit", ylabel='ylabel', yunit="yunit"):
    gp.figure(figure)
    gp.s([x, y],'tmp_plot.dat')
    gp.c('set title "' + title + '"')
    gp.c('set xlabel "' + xlabel + ' [' + xunit + ']"')
    gp.c('set ylabel "' + ylabel + ' [' + yunit + ']"')
    gp.c('set grid')
    gp.c('unset key')
    gp.c('plot "tmp_plot.dat" lc rgb "#8b1a0e" w l')


# change file name
file_name = file_name.replace('.dat','')
file_name = file_name.replace('.hea','')
# reading MIT file
record = wfdb.rdsamp(file_name)
# create time vector
time = np.linspace(0, record[1]['sig_len']/record[1]['fs'], record[1]['sig_len'])
# create signal vector
signal = np.concatenate(record[0])
# resampling signal
signal_resample = processing.resample_sig(signal, record[1]['fs'], frequency)
# create time vector
time_resample = np.linspace(0, len(signal_resample[0])/frequency, len(signal_resample[0]))
ipdb.set_trace()
#>>> # Read part of a record from Physiobank
#>>> signals, fields = wfdb.rdsamp('a103l', sampfrom=50000, channels=[0,1],
#                               pb_dir='challenge/2015/training')
#>>> # Write a local WFDB record (manually inserting fields)
#>>> wfdb.wrsamp('ecgrecord', fs = 250, units=['mV', 'mV'],
#                sig_name=['I', 'II'], p_signal=signals, fmt=['16', '16'])
wfdb.wrsamp(file_name.split('/')[-1] + '_resampled_' + str(frequency),
fs = frequency, units = record[1]['units'],
fmt=["16"],
sig_name = record[1]['sig_name'],
p_signal = np.asarray(signal_resample[0].reshape(len(signal_resample[0]), 1)) )
