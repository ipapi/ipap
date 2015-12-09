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
        flatshape = (image.data.shape[0], image.data.shape[1])
        rdata = np.reshape(np.delete(image.data, [1, 2, 3], 2), flatshape)
        gdata = np.reshape(np.delete(image.data, [0, 2, 3], 2), flatshape)
        bdata = np.reshape(np.delete(image.data, [0, 1, 3], 2), flatshape)
        adata = np.reshape(np.delete(image.data, [0, 1, 2], 2), flatshape)
        image._dft = np.array([
            np.fft.fft2(rdata),
            np.fft.fft2(gdata),
            np.fft.fft2(bdata),
            np.fft.fft2(adata)
        ])

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
        size = self._dft[0].shape[0]
        self.data = np.concatenate(
            (
                np.split(np.fft.ifft2(self._dft[0]).astype(np.uint8), size, axis=1),
                np.split(np.fft.ifft2(self._dft[1]).astype(np.uint8), size, axis=1),
                np.split(np.fft.ifft2(self._dft[2]).astype(np.uint8), size, axis=1),
                np.split(np.fft.ifft2(self._dft[3]).astype(np.uint8), size, axis=1)
            ),
            axis=2
        )

    @property
    def dft_magnitude(self):
        oldshape = self.dft[0].shape
        shape = (oldshape[0], oldshape[1], 1)
        rgba = np.concatenate(
            (
                np.split(np.fft.fftshift(self.dft[0]) / 65000 * 255, self.dft[0].shape[0], axis=1),
                np.split(np.fft.fftshift(self.dft[1]) / 65000 * 255, self.dft[1].shape[0], axis=1),
                np.split(np.fft.fftshift(self.dft[2]) / 65000 * 255, self.dft[2].shape[0], axis=1),
                np.ones(shape) * 255
            ),
            axis=2
        )

        return abs(rgba).astype(np.uint8)

    @property
    def dft_real(self):
        return self.dft.real

    @property
    def dft_imag(self):
        return self.dft.imag
