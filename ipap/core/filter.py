from math import sqrt, exp

import numpy as np


def distance(u, v, dft):
    return sqrt((u - (dft.shape[0] / 2))**2 + (v - (dft.shape[1] / 2))**2)


def lowpass_ideal(value, cutoff):
    if value <= cutoff:
        return 1
    else:
        return 0


def highpass_ideal(value, cutoff):
    if (value > cutoff):
        return 1
    else:
        return 0


def bandreject_ideal(value, cutoff, width):
    offset = cutoff + width / 2
    if (-offset <= value <= offset):
        return 0
    else:
        return 1


def bandpass_ideal(value, cutoff, width):
    offset = cutoff + width / 2
    if (-offset <= value <= offset):
        return 1
    else:
        return 0


def lowpass_gauss(value, cutoff):
    return exp(-(value**2) / (2 * cutoff**2))


def highpass_gauss(value, cutoff):
    return exp(-(value**2 / (2 * cutoff**2)))


def lowpass_butterworth(value, cutoff, n):
    return 1 / (1 + (value / cutoff)**(2*n))


def highpass_butterworth(value, cutoff, n):
    return 1 / (1 + (cutoff / value)**(2*n))


def apply_filter(data, filter):
    filtered = np.zeros(data.shape)
    for u in range(0, data.shape[0]):
        for v in range(0, data.shape[1]):
            value = distance(u, v, data)
            filtered[u][v] = data[u][v] * filter(value)

    return filtered


def ideal(filtertype, data, cutoff):
    def filter(value):
        func = globals()[filtertype + '_ideal']
        return func(value, cutoff)

    return apply_filter(data, filter)


def gauss(filtertype, data, cutoff):
    def filter(value):
        func = globals()[filtertype + '_gauss']
        return func(value, cutoff)

    return apply_filter(data, filter)
