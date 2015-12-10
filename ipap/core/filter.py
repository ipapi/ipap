from math import sqrt, exp

import numpy as np


def distance(u, v, dft):
    return sqrt((u - (dft.shape[0] / 2))**2 + (v - (dft.shape[1] / 2))**2)


def ideal(value, cutoff, ftype='lowpass', bwidth=1.0):
    if ftype == 'lowpass':
        return 1 if value <= cutoff else 0
    elif ftype == 'highpass':
        return 0 if value <= cutoff else 1
    elif ftype == 'bandreject':
        min = cutoff - (bwidth / 2)
        max = cutoff + (bwidth / 2)
        return 0 if min <= value <= max else 1
    elif ftype == 'bandpass':
        min = cutoff - (bwidth / 2)
        max = cutoff + (bwidth / 2)
        return 1 if min <= value <= max else 0


def gauss(value, cutoff, ftype='lowpass', bwidth=1.0):
    if ftype == 'lowpass':
        return exp(-(value**2) / (2 * cutoff**2))
    elif ftype == 'highpass':
        return 1 - exp(-(value**2 / (2 * cutoff**2)))
    elif ftype == 'bandreject':
        return 1 - exp(-((value**2 - cutoff**2) / ((1+value) * bwidth))**2)
    elif ftype == 'bandpass':
        return exp(-((value**2 - cutoff**2) / ((1+value) * bwidth))**2)


def butterworth(value, cutoff, n, ftype='lowpass', bwidth=1.0):
    if ftype == 'lowpass':
        return 1 / (1 + (value / cutoff)**(2*n))
    elif ftype == 'highpass':
        return 1 / (1 + (cutoff / (1+value))**(2*n))
    elif ftype == 'bandreject':
        return 1 / (1 + ((value * bwidth) / (1+(value**2 - cutoff**2)))**(2*n))
    elif ftype == 'bandpass':
        return 1 / (1 + ((value**2 - cutoff**2) / ((1+value) * bwidth))**(2*n))


def apply_filter(data, filter):
    filtered = np.empty(data.shape, dtype=complex)
    for c in range(0, data.shape[0]):
        for u in range(0, data.shape[1]):
            for v in range(0, data.shape[2]):
                value = distance(u, v, data[c])
                filtered[c][u][v] = data[c][u][v] * filter(value)

    return filtered
