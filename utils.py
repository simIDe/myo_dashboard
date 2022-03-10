import numpy as np
from scipy import signal


def envelope(emg, sample_rate, low_pass=3, order=5):
    """Apply a low pass filter to get the enveloppe of the emg signal

    Args:
        emg (numpy.array): The emg signal
        sample_rate (int): Sample rate of the signal
        low_pass (int, optional): Low frequency of the low-pass filter. Defaults to 10.
        order (int, optional): Order of the band-pass filter. Defaults to 4.

    Returns:
        numpy.array: filtered signal
    """
    low_pass = low_pass/(sample_rate/2)
    b, a = signal.butter(order, low_pass, btype='lowpass')
    if 3 * max(len(a), len(b)) < len(emg):
        emg_envelope = signal.filtfilt(b, a, emg)
    else:
        emg_envelope = np.full(100, 0)
    return emg_envelope


def band_pass(emg, sample_rate, high_pass=20, low_pass=450, order=4):
    """Apply a band-pass butterworth filter

    Args:
        emg (numpy.array): The emg signal
        sample_rate (int): Sample rate of the signal
        high_pass (int, optional): High frequency of the band-pass filter. Defaults to 20.
        low_pass (int, optional): Low frequency of the band-pass filter. Defaults to 450.
        order (int, optional): Order of the band-pass filter. Defaults to 4.

    Returns:
        numpy.array: The filtered signal
    """
    emg = emg[~np.isnan(emg)]
    # cut-off frequency/Nyquist frequency
    high_pass = high_pass/(sample_rate/2)
    low_pass = low_pass/(sample_rate/2)
    b, a = signal.butter(order, [high_pass, low_pass], btype='bandpass')
    # emg_correctmean = emg - np.mean(emg)
    if 3 * max(len(a), len(b)) < len(emg):
        emg_filt = signal.filtfilt(b, a, emg)
    else:
        emg_filt = np.full(len(emg), 0)
        # TODO: Warning signal here
        # Manage this case
    return emg_filt
