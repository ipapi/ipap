from PIL import Image as PilImage
import numpy as np


class Image:
    def __init__(self):
        self.data = np.array([])

        self._pil = None
        self._dft = np.array([])

    def from_pil(pilimage):
        # Hacky, hacky, hacky, but required for 32-bit alignment (Qt)
        pilimage = pilimage.convert('RGBA')

        image = Image()

        image.data = np.asarray(pilimage, dtype=np.uint8)
        image._pil = pilimage
        image._dft = np.fft.fft2(image.data)

        return image

    def from_file(filepath):
        return Image.from_pil(PilImage.open(filepath))

    def getmode(self):
        return self._pil.mode

    @property
    def dft(self):
        return self._dft

    @dft.setter
    def dft(self, data):
        self._dft = data
        self.data = np.fft.ifft2(self._dft).real.astype(np.uint8)

    @property
    def dft_magnitude(self):
        return abs(self.dft)

    @property
    def dft_real(self):
        return self.dft.real

    @property
    def dft_imag(self):
        return self.dft.imag
