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

        image._rgb = np.array([
            rdata,
            gdata,
            bdata
        ])

        image._dft = np.array([
            np.fft.fftshift(np.fft.fft2(rdata)),
            np.fft.fftshift(np.fft.fft2(gdata)),
            np.fft.fftshift(np.fft.fft2(bdata))
        ])

        image._update_data()

        return image

    def from_file(filepath):
        return Image.from_pil(PilImage.open(filepath))

    def getmode(self):
        return self._pil.mode

    def _update_data(self):
        self.data = np.empty((self._rgb[0].shape[0], self._rgb[0].shape[1], 4), dtype=np.uint8)
        for row in range(0, self.data.shape[0]):
            for col in range(0, self.data.shape[1]):
                for chan in range(0, 3):
                    self.data[row][col][chan] = self._rgb[chan][row][col]
                self.data[row][col][3] = 255

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
    def rgb(self):
        return self._rgb

    @property
    def dft(self):
        return self._dft

    @dft.setter
    def dft(self, dft_data):
        self._dft = dft_data

        self._rgb = np.array([
            np.fft.ifft2(np.fft.ifftshift(self._dft[0])).astype(np.uint8),
            np.fft.ifft2(np.fft.ifftshift(self._dft[1])).astype(np.uint8),
            np.fft.ifft2(np.fft.ifftshift(self._dft[2])).astype(np.uint8)
        ])

        self._update_data()

    @property
    def dft_rgb(self):
        rgb = np.concatenate(
            (
                np.split(self.dft[0], self.dft[0].shape[1], axis=1),
                np.split(self.dft[1], self.dft[1].shape[1], axis=1),
                np.split(self.dft[2], self.dft[2].shape[1], axis=1)
            ),
            axis=2
        )
        rgb = np.transpose(rgb, axes=[1, 0, 2])

        return rgb

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

    @property
    def dft_phase(self):
        rgb = np.angle(self.dft_rgb)
        rgb = rgb * (255 / np.amax(rgb))

        return self._add_alpha(rgb).astype(np.uint8)
