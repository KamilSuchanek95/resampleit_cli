#import argparse
import numpy as np
import scipy.signal as sig
import wfdb
from wfdb import processing
from zenipy import file_selection
import ipdb

#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('Path', metavar='p', type=str,
#help='path to the file with the .dat or .hea signal')

# arguments
#args = parser.parse_args()
#ipdb.set_trace()

file_name = file_selection(multiple=False, directory=False, save=False, confirm_overwrite=False, filename=None, title='', width=330, height=120, timeout=None)
frequency = int(input("Enter target frequency: "))

#ipdb.set_trace()

# change file name
file_name = file_name.replace('.dat','')
file_name = file_name.replace('.hea','')

# reading MIT file
record = wfdb.rdsamp(file_name)

# create signal vector
signal = np.concatenate(record[0])

# resampling signal
signal_resample = processing.resample_sig(signal, record[1]['fs'], frequency)

wfdb.wrsamp(file_name.split('/')[-1] + '_resampled_' + str(frequency),
fs = frequency, units = record[1]['units'],
fmt=["16"],
sig_name = record[1]['sig_name'],
p_signal = np.asarray(signal_resample[0].reshape(len(signal_resample[0]), 1)) )

print('Signal was resampled from %i [Hz] to %i [Hz]\n' %(record[1]['fs'], frequency))
print('The resulting files are located in the current folder\n')
