# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 00:49:39 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

def max_level_3oct(data_all_signals, fs, f_min, f_max):
    """Return the maximum value of the frequency bands you choose. Each one is calculated with the levels (dB)
    of its band in the different signals.

    Parameters
    ----------
    data_all_signals : numpy.ndarray
        Array which each row corresponds to the data of a signal [Pa].
    fs : float
        Sampling frequency [Hz].
    fmax : float
        Max frequency band [Hz].
    fmin : float
        Min frequency band [Hz].

    Outputs
    -------
    max_level_3oct : numpy.ndarray
        The maximum values of each frequency band.
    """
    # We initialize the array that stores the third octave values (in Pa) of the all signals ​​with the first signal.
    spectrum_all_signals_Pa = noct_spectrum(data_all_signals[0],fs,f_min,f_max)[0]
    # We initialize the center frequencies of the third octaves with the first signal.
    freq = noct_spectrum(data_all_signals[0],fs,f_min,f_max)[1]
    # We initialize the number of the signals.
    num_signals = data_all_signals.shape[0]
    # We initialize the number of frequency bands.
    num_bands = freq.shape[0]

    # Calculate the value of the third octave in Pa of each signal.
    for i in range(num_signals):
        # We skip the first signal because we have initialized with it.
        if i != 0:
            # We calculate and save the values ​​of the third octaves of the signals
            spectrum_all_signals_Pa = np.append(spectrum_all_signals_Pa,noct_spectrum(data_all_signals[i],fs,f_min,f_max)[0],axis=1)

    # Creating a list of zeros of the size of the frequency bands (to keep the maximum level values).
    max_level_3oct = np.zeros(num_bands)
    # Empty array to store the values in dB of the third octave whose maximum value is going to be calculated.
    band_value_all_signals = np.zeros(num_signals)
    # For each frequency band you perform the operation.
    for i in range(num_bands):
        # Performs the conversion to dB with all the values of the frequency band in the different signals.
        for j in range(num_signals): 
            # Conversion Pa to dB.
            dB = amp2db(np.array(spectrum_all_signals_Pa[i][j]))
            # Save all values in dB of the third octave in another array.
            band_value_all_signals[j] = dB
        # Calculate and keep the maximum value found in the array. That value will be the maximum of the third of an octave.
        max_level_3oct[i] = max(band_value_all_signals)
    
    print("frecuencias centrales")
    print(freq)
    print("El valor max de cada banda del tercio de octava")
    
    return max_level_3oct


if __name__ == "__main__":
    
    sig_1, fs_1 = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    print("Una señal de ruido rosa 60 dB despues del load")
    print(sig_1)
    print(sig_1.shape)
    print("frecuencia de muestreo")
    print(fs_1)

    sig_2, fs_2 = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    print("Una señal de tono puro 1 KHZ 10 ms 70 dB despues del load")
    print(sig_2)
    print(sig_2.shape)
    print("frecuencia de muestreo")
    print(fs_2)
    sig_3, fs_3 = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")

    data_all_signals = np.stack((sig_1,sig_2,sig_3))
    print("Data all signals de tres .wav")
    print(data_all_signals)
    print(data_all_signals.shape[0])
    print(data_all_signals.shape[1])

    ########## Validacion
     # [10, 20, 30, ... 100]
    validacion_1 = np.array([0.00006324555320337, 0.0002, 0.0006324555320337, 0.002, 0.006324555320337, 0.02, 
    0.06324555320337, 0.2, 0.6324555320337, 2])
    print(validacion_1)

    validacion_2 = np.array([0.00006324555320337, 0.0002, 0.0006324555320337, 0.002, 0.006324555320337, 0.02, 
    0.06324555320337, 0.2, 0.6324555320337, 2])

    validacion_3 = np.array([0.00006324555320337, 0.0002, 0.0006324555320337, 0.002, 0.006324555320337, 0.02, 
    0.06324555320337, 0.2, 0.6324555320337, 2])

    all_validaciones = np.stack((validacion_1,validacion_2,validacion_3))
    ##################

    f_min = 250
    f_max =20000
    fs = fs_1

    max = max_level_3oct(data_all_signals,fs,f_min,f_max)
    print(max)

    pass
