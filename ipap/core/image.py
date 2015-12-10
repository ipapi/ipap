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

        image._pil = pilimage
        image.data = np.asarray(pilimage, dtype=np.uint8)

        rdata = np.reshape(np.asarray(pilimage.getdata(band=0)), pilimage.size[::-1])
        gdata = np.reshape(np.asarray(pilimage.getdata(band=1)), pilimage.size[::-1])
        bdata = np.reshape(np.asarray(pilimage.getdata(band=2)), pilimage.size[::-1])
        adata = np.reshape(np.asarray(pilimage.getdata(band=3)), pilimage.size[::-1])

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
        size = self._dft[0].shape[1]
        data = np.concatenate(
            (
                np.split(np.fft.ifft2(self._dft[0]).astype(np.uint8), size, axis=1),
                np.split(np.fft.ifft2(self._dft[1]).astype(np.uint8), size, axis=1),
                np.split(np.fft.ifft2(self._dft[2]).astype(np.uint8), size, axis=1),
                np.split(np.fft.ifft2(self._dft[3]).astype(np.uint8), size, axis=1)
            ),
            axis=2
        )
        self.data = np.transpose(data, axes=[1, 0, 2])

    @property
    def dft_rgb(self):
        rgb = np.concatenate(
            (
                np.split(np.fft.fftshift(self.dft[0]), self.dft[0].shape[1], axis=1),
                np.split(np.fft.fftshift(self.dft[1]), self.dft[1].shape[1], axis=1),
                np.split(np.fft.fftshift(self.dft[2]), self.dft[2].shape[1], axis=1)
            ),
            axis=2
        )
        rgb = np.transpose(rgb, axes=[1, 0, 2])

        return rgb

    def _add_alpha(self, rgb):
        oldshape = self.dft[0].shape
        return np.concatenate(
            (
                rgb,
                np.ones((oldshape[0], oldshape[1], 1)) * 255
            ),
            axis=2
        )

    @property
    def dft_magnitude(self):
        rgb = np.log(abs(self.dft_rgb))
        rgb = rgb * (255 / np.amax(rgb))

        return self._add_alpha(rgb).astype(np.uint8)

    @property
    def dft_real(self):
        rgb = np.log(abs(self.dft_rgb.real))
        rgb = rgb * (255 / np.amax(rgb))

        return self._add_alpha(rgb).astype(np.uint8)

    @property
    def dft_imag(self):
        rgb = np.log(abs(self.dft_rgb.imag))
        rgb = rgb * (255 / np.amax(rgb))

        return self._add_alpha(rgb).astype(np.uint8)
