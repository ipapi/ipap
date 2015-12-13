import numpy as np

import ipap.core.filter as filter
from ipap.core.image import Image

class ImageProcessor:
    def __init__(self):
        self.original = Image()
        self.output = Image()

        # None, 'lowpass', 'highpass', 'bandpass', 'bandreject'
        self.filter_type = None

        # 'ideal', 'butterworth', 'gauss'
        self.filter_function = 'ideal'

        # Cutoff frequency for the filter
        self.filter_cutoff = 1.0

        # Width of the band when using 'bandpass' or 'bandreject'
        self.band_width = 1.0

        # nth order when using butterworth
        self.order = 1.0

    def _ideal(self, value):
        return filter.ideal(value, self.filter_cutoff, ftype=self.filter_type, bwidth=self.band_width)

    def _gauss(self, value):
        return filter.gauss(value, self.filter_cutoff, ftype=self.filter_type, bwidth=self.band_width)

    def _butterworth(self, value):
        return filter.butterworth(value, self.filter_cutoff, self.order, ftype=self.filter_type, bwidth=self.band_width)

    def apply(self):
        print("Applying {}_{} with cutoff {} and bandwidth {}".format(self.filter_type,
                                                                      self.filter_function,
                                                                      self.filter_cutoff,
                                                                      self.band_width))
        if self.filter_type is None:
            self.output.dft = self.original.dft
        else:
            if self.filter_function == 'ideal':
                self.output.dft = filter.apply_filter(self.original.dft, lambda value: self._ideal(value))
            if self.filter_function == 'gauss':
                self.output.dft = filter.apply_filter(self.original.dft, lambda value: self._gauss(value))
            if self.filter_function == 'butterworth':
                self.output.dft = filter.apply_filter(self.original.dft, lambda value: self._butterworth(value))

    def mse(self):
        error = np.sum((self.original.rgb - self.output.rgb) ** 2)
        error /= self.original.rgb.size
        return error
