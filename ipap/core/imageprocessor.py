import ipap.core.filter as filter
from ipap.core.image import Image


class ImageProcessor:
    def __init__(self):
        self.original = Image()
        self.output = Image()

        # None, 'lowpass', 'highpass', 'bandpass', 'bandreject'
        self.filter_type = None

        # None, 'ideal', 'butterworth', 'gauss'
        self.filter_function = None

        # Cutoff frequency for the filter
        self.filter_cutoff = 1.0

        # Width of the band when using 'bandpass' or 'bandreject'
        self.band_width = 1.0

    def apply(self):
        if self.filter_function == 'ideal':
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
        else:
            self.output.dft = self.original.dft
