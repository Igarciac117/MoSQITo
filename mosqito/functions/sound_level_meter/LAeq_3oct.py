# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:02:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np
from sympy import zeros

# Local imports
from Leq_3oct import Leq_3oct
from mosqito.functions.shared.A_weighting import A_weighting
from mosqito.functions.shared.load import load
from mosqito.functions.oct3filter.calc_third_octave_levels import calc_third_octave_levels

def LAeq_3oct (spectrum_signal_samples,freq):
    """Calculate the LAeq of the frequency bands you choose, returns the calculated LAeq values for each band.
    Each one is calculated with the levels (dBA) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each column is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the LAeq.

    Outputs
    -------
    LAeq_3oct : numpy.ndarray
        a list of the Leq values (dBA) for each frequency band.
    """
    # Empty list to keep the lists. Each list is the dBA values for each frequency band in a sample. 
    signal_sample_A = []
    # Take the columns of the array one by one and perform the function to transform the values in dB to dBA.
    for i in range(spectrum_signal_samples.shape[1]):
        # Save dBA values lists in the list "signal_sample_A".
        signal_sample_A.append(A_weighting(spectrum_signal_samples.T[i],freq))
    # Create an array in which each list of "signal_sample_A" is a column of the array. 
    spectrum_signal_samples_A = np.array(signal_sample_A)
    # Calculate Leq of each frequency bands with the new dBA values.
    LAeq_3oct = Leq_3oct(spectrum_signal_samples_A, freq)
    
    return LAeq_3oct


if __name__ == "__main__":
    
    sig, fs = load(True,r"Programas_y_repositorios\MoSQITo\tests\input\white_noise_200_2000_Hz_stationary.wav", calib=1)

    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])

    LAeq = LAeq_3oct(spectrum_signal_samples,freq)
    print(LAeq)
    pass