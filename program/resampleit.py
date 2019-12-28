"""RESAMPLE IT CLI
Usage:
    resampleit.py
    resampleit.py <target_frequency> <path>
    resampleit.py -h|--help
    resampleit.py -v|--version
Options:
    <path>  Full path to the record file with the extension .dat or .hea.
    <target_frequency>  Target sampling rate.
    -h --help  Show this screen.
    -v --version  Show version.
"""

from docopt import docopt
import numpy
import wfdb
from wfdb import processing
from zenipy import file_selection

def resampleit(path, target_frequency):

    # change file name
    path = path.replace('.dat','')
    path = path.replace('.hea','')

    # reading MIT file
    record = wfdb.rdsamp(path)

    # create signal vector
    signal = numpy.concatenate(record[0])

    # resampling signal
    signal_resample = processing.resample_sig(signal, record[1]['fs'], target_frequency)

    wfdb.wrsamp(path.split('/')[-1] + '_resampled_to' + str(target_frequency),
    fs = target_frequency, units = record[1]['units'],
    fmt=["16"],
    sig_name = record[1]['sig_name'],
    p_signal = numpy.asarray(signal_resample[0].reshape(len(signal_resample[0]), 1)) )

    print('Signal was resampled from %i [Hz] to %i [Hz]\n' %(record[1]['fs'], target_frequency))
    print('The resulting files are located in the current folder\n')

if __name__ == '__main__':
    arguments = docopt(__doc__, version=' 1.0')
    if arguments['<path>'] and arguments['<target_frequency>']:
        resampleit(arguments['<path>'], arguments['<target_frequency>'])
    else:
        path = file_selection(multiple=False, directory=False, save=False, confirm_overwrite=False, filename=None, title='', width=330, height=120, timeout=None)
        target_frequency = int(input("Enter target frequency: "))
        resampleit(path, target_frequency)
