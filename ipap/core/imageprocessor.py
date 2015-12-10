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

    def apply(self):
        print("Applying {}_{} with cutoff {} and bandwidth {}".format(self.filter_type,
                                                                      self.filter_function,
                                                                      self.filter_cutoff,
                                                                      self.band_width))
        if self.filter_type is None:
            self.output.dft = self.original.dft
        elif self.filter_function == 'ideal':
            self.output.dft = filter.ideal(self.filter_type,
                                           self.original.dft,
                                           self.filter_cutoff)
        elif self.filter_function == 'gauss':
            self.output.dft = filter.gauss(self.filter_type,
                                           self.original.dft,
                                           self.filter_cutoff)
        elif self.filter_function == 'butterworth':
            self.output.dft = filter.butterworth(self.filter_type,
                                                 self.original.dft,
                                                 self.filter_cutoff,
                                                 self.filter_order)

    def mse(self):
        #self.original._pil.getdata(band=0)
        #self.output._pil.getdata(band=0)
        error = np.sum((self.original.data - self.output.data) ** 2)
        error /= float(self.original.data.shape[0] * self.output.data.shape[1])
        return error
