import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QAction,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QStatusBar,
    QDockWidget,
    QFormLayout,
    QGroupBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
    QGridLayout,
    QFrame,
    QVBoxLayout
)

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QImage, QPixmap, QColor

from ipap.core.imageprocessor import ImageProcessor
from ipap.core.image import Image


def grayscale_colortable():
    table = []
    for i in range(0, 256):
        color = QColor(i, i, i)
        table.append(color.rgb())
    return table


def make_qimage(image):
    imageformat = QImage.Format_RGBA8888
    imagedata = image.data
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    return qimage


def make_dftmag_qimage(image):
    imageformat = QImage.Format_RGBA8888
    imagedata = image.dft_magnitude
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    return qimage


def make_dftreal_qimage(image):
    imageformat = QImage.Format_RGBA8888
    imagedata = image.dft_real
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    return qimage


def make_dftimag_qimage(image):
    imageformat = QImage.Format_RGBA8888
    imagedata = image.dft_imag
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    return qimage


def make_dftphase_qimage(image):
    imageformat = QImage.Format_RGBA8888
    imagedata = image.dft_phase
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    return qimage


class MainWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self._app = app

        self._type_none = 0
        self._type_lowpass = 1
        self._type_highpass = 2
        self._type_bandreject = 3
        self._type_bandaccept = 4
        self._function_ideal = 0
        self._function_butterworth = 1
        self._function_gaussion = 2

        self.processor = ImageProcessor()
        self.initui()

    def initui(self):
        self.initmenubar()
        self.initoptionspanel()
        self.initlabels()
        centralwidget = self.initcentralwidget()
        self.setCentralWidget(centralwidget)
        self.statusBar()
        self.setWindowTitle("Ipap")

    def initlabels(self):
        # Initialize image containers
        self.originalimage_container = QLabel('Placeholder')
        self.originalimage_magnitude_container = QLabel('laceholder')
        self.originalimage_realpart_container = QLabel('Placeholder')
        self.originalimage_imaginarypart_container = QLabel('Placeholder')
        self.originalimage_phase_container = QLabel('Placeholder')
        self.reconstructedimage_container = QLabel('Placeholder')
        self.reconstructedimage_magnitude_container = QLabel('Placeholder')
        self.reconstructedimage_realpart_container = QLabel('Placeholder')
        self.reconstructedimage_imaginarypart_container = QLabel('Placeholder')
        self.reconstructedimage_phase_container = QLabel('Placeholder')

        # Original image container layout
        originalimage_boxlayout = QVBoxLayout()
        originalimage_boxlayout.addWidget(QLabel('Original Image'))
        originalimage_boxlayout.addWidget(self.originalimage_container)
        originalimage_magnitude_boxlayout = QVBoxLayout()
        originalimage_magnitude_boxlayout.addWidget(QLabel('Magnitude'))
        originalimage_magnitude_boxlayout.addWidget(self.originalimage_magnitude_container)
        originalimage_realpart_boxlayout = QVBoxLayout()
        originalimage_realpart_boxlayout.addWidget(QLabel('Real Part'))
        originalimage_realpart_boxlayout.addWidget(self.originalimage_realpart_container)
        originalimage_imaginarypart_boxlayout = QVBoxLayout()
        originalimage_imaginarypart_boxlayout.addWidget(QLabel('Imaginary Part'))
        originalimage_imaginarypart_boxlayout.addWidget(self.originalimage_imaginarypart_container)
        originalimage_phase_boxlayout = QVBoxLayout()
        originalimage_phase_boxlayout.addWidget(QLabel('Phase'))
        originalimage_phase_boxlayout.addWidget(self.originalimage_phase_container)

        # Reconstructed image container layout
        reconstructedimage_boxlayout = QVBoxLayout()
        reconstructedimage_boxlayout.addWidget(QLabel('Reconstructed Image'))
        reconstructedimage_boxlayout.addWidget(self.reconstructedimage_container)
        reconstructedimage_magnitude_boxlayout = QVBoxLayout()
        reconstructedimage_magnitude_boxlayout.addWidget(QLabel('Magnitude'))
        reconstructedimage_magnitude_boxlayout.addWidget(self.reconstructedimage_magnitude_container)
        reconstructedimage_realpart_boxlayout = QVBoxLayout()
        reconstructedimage_realpart_boxlayout.addWidget(QLabel('Real Part'))
        reconstructedimage_realpart_boxlayout.addWidget(self.reconstructedimage_realpart_container)
        reconstructedimage_imaginarypart_boxlayout = QVBoxLayout()
        reconstructedimage_imaginarypart_boxlayout.addWidget(QLabel('Imaginary Part'))
        reconstructedimage_imaginarypart_boxlayout.addWidget(self.reconstructedimage_imaginarypart_container)
        reconstructedimage_phase_boxlayout = QVBoxLayout()
        reconstructedimage_phase_boxlayout.addWidget(QLabel('Phase'))
        reconstructedimage_phase_boxlayout.addWidget(self.reconstructedimage_phase_container)

        # Widgets holding a title and an image
        self.originalimage_box = QWidget()
        self.originalimage_magnitude_box = QWidget()
        self.originalimage_realpart_box = QWidget()
        self.originalimage_imaginarypart_box = QWidget()
        self.originalimage_phase_box = QWidget()
        self.reconstructedimage_box = QWidget()
        self.reconstructedimage_magnitude_box = QWidget()
        self.reconstructedimage_realpart_box = QWidget()
        self.reconstructedimage_imaginarypart_box = QWidget()
        self.reconstructedimage_phase_box = QWidget()

        # Set corresponding layout to each widget
        self.originalimage_box.setLayout(originalimage_boxlayout)
        self.originalimage_magnitude_box.setLayout(originalimage_magnitude_boxlayout)
        self.originalimage_realpart_box.setLayout(originalimage_realpart_boxlayout)
        self.originalimage_imaginarypart_box.setLayout(originalimage_imaginarypart_boxlayout)
        self.originalimage_phase_box.setLayout(originalimage_phase_boxlayout)
        self.reconstructedimage_box.setLayout(reconstructedimage_boxlayout)
        self.reconstructedimage_magnitude_box.setLayout(reconstructedimage_magnitude_boxlayout)
        self.reconstructedimage_realpart_box.setLayout(reconstructedimage_realpart_boxlayout)
        self.reconstructedimage_imaginarypart_box.setLayout(reconstructedimage_imaginarypart_boxlayout)
        self.reconstructedimage_phase_box.setLayout(reconstructedimage_phase_boxlayout)

    def updateimages(self):
        # Get pixelmap of each image
        originalimage_pixelmap = QPixmap.fromImage(make_qimage(self.processor.original))
        originalimage_magnitude_pixelmap = QPixmap.fromImage(make_dftmag_qimage(self.processor.original))
        originalimage_realpart_pixelmap = QPixmap.fromImage(make_dftreal_qimage(self.processor.original))
        originalimage_imaginarypart_pixelmap = QPixmap.fromImage(make_dftimag_qimage(self.processor.original))
        originalimage_phase_pixelmap = QPixmap.fromImage(make_dftphase_qimage(self.processor.original))
        reconstructedimage_pixelmap = QPixmap.fromImage(make_qimage(self.processor.output))
        reconstructedimage_magnitude_pixelmap = QPixmap.fromImage(make_dftmag_qimage(self.processor.output))
        reconstructedimage_realpart_pixelmap = QPixmap.fromImage(make_dftreal_qimage(self.processor.output))
        reconstructedimage_imaginarypart_pixelmap = QPixmap.fromImage(make_dftimag_qimage(self.processor.output))
        reconstructedimage_phase_pixelmap = QPixmap.fromImage(make_dftphase_qimage(self.processor.output))

        # Scale each image by 200 x 200
        originalimage_pixelmap = originalimage_pixelmap.scaled(250,250, Qt.KeepAspectRatio)
        originalimage_magnitude_pixelmap = originalimage_magnitude_pixelmap.scaled(100,100, Qt.KeepAspectRatio)
        originalimage_realpart_pixelmap = originalimage_realpart_pixelmap.scaled(100,100, Qt.KeepAspectRatio)
        originalimage_imaginarypart_pixelmap = originalimage_imaginarypart_pixelmap.scaled(100,100, Qt.KeepAspectRatio)
        originalimage_phase_pixelmap = originalimage_phase_pixelmap.scaled(100,100, Qt.KeepAspectRatio)
        reconstructedimage_pixelmap = reconstructedimage_pixelmap.scaled(250,250, Qt.KeepAspectRatio)
        reconstructedimage_magnitude_pixelmap = reconstructedimage_magnitude_pixelmap.scaled(100,100, Qt.KeepAspectRatio)
        reconstructedimage_realpart_pixelmap = reconstructedimage_realpart_pixelmap.scaled(100,100, Qt.KeepAspectRatio)
        reconstructedimage_imaginarypart_pixelmap = reconstructedimage_imaginarypart_pixelmap.scaled(100,100, Qt.KeepAspectRatio)
        reconstructedimage_phase_pixelmap = reconstructedimage_phase_pixelmap.scaled(100,100, Qt.KeepAspectRatio)

        # Update image containers
        self.originalimage_container.setPixmap(originalimage_pixelmap)
        self.originalimage_magnitude_container.setPixmap(originalimage_magnitude_pixelmap)
        self.originalimage_realpart_container.setPixmap(originalimage_realpart_pixelmap)
        self.originalimage_imaginarypart_container.setPixmap(originalimage_imaginarypart_pixelmap)
        self.originalimage_phase_container.setPixmap(originalimage_phase_pixelmap)
        self.reconstructedimage_container.setPixmap(reconstructedimage_pixelmap)
        self.reconstructedimage_magnitude_container.setPixmap(reconstructedimage_magnitude_pixelmap)
        self.reconstructedimage_realpart_container.setPixmap(reconstructedimage_realpart_pixelmap)
        self.reconstructedimage_imaginarypart_container.setPixmap(reconstructedimage_imaginarypart_pixelmap)
        self.reconstructedimage_phase_container.setPixmap(reconstructedimage_phase_pixelmap)

        error = self.processor.mse()
        self.mselabel.setNum(error)

    def initmenubar(self):
        openfile_other = QAction('Open File', self)
        openfile_other.setShortcut('Ctrl+O')
        openfile_other.setStatusTip('Open File')
        openfile_other.triggered.connect(lambda: self.opendialog(QDir.homePath()))

        openfile_db = QAction('Open from DB', self)
        openfile_db.setShortcut('Ctrl+Shift+O')
        openfile_db.setStatusTip('Open file from database')
        openfile_db.triggered.connect(lambda: self.opendialog('images'))

        exitprogram = QAction('Quit', self)
        exitprogram.setShortcut('Ctrl+Q')
        exitprogram.setStatusTip('Exit the application')
        exitprogram.triggered.connect(self._app.closeAllWindows)

        menufile = self.menuBar().addMenu('File')
        menufile.addAction(openfile_other)
        menufile.addAction(openfile_db)
        menufile.addSeparator()
        menufile.addAction(exitprogram)

    def initoptionspanel(self):
        label = QLabel('Filter')

        filtertype = QComboBox()
        filtertype.addItem('None')
        filtertype.addItem('Lowpass')
        filtertype.addItem('Highpass')
        filtertype.addItem('Bandreject')
        filtertype.addItem('Bandaccept')
        filtertype.currentIndexChanged.connect(self.filtertypelistener)

        self.filterfunction = QComboBox()
        self.filterfunction.addItem('Ideal')
        self.filterfunction.addItem('Butterworth')
        self.filterfunction.addItem('Gaussion')
        self.filterfunction.currentIndexChanged.connect(self.filterfunctionlistener)
        self.filterfunction.setEnabled(False)

        self.filtercutoff = QDoubleSpinBox()
        self.filtercutoff.setValue(0.0)
        self.filtercutoff.setRange(-1000.0, 1000.0)
        self.filtercutoff.valueChanged.connect(self.filtercutofflistener)
        self.filtercutoff.setEnabled(False)

        self.filterbandwidth = QDoubleSpinBox()
        self.filterbandwidth.setValue(0.0)
        self.filterbandwidth.setRange(-1000.0, 1000.0)
        self.filterbandwidth.valueChanged.connect(self.filterbandwidthlistener)
        self.filterbandwidth.setEnabled(False)

        self.filterorder = QDoubleSpinBox()
        self.filterorder.setValue(1.0)
        self.filterorder.setRange(-1000.0, 1000.0)
        self.filterorder.valueChanged.connect(self.filterorderlistener)
        self.filterorder.setEnabled(False)

        formlayout = QFormLayout()
        formlayout.addRow('Type', filtertype)
        formlayout.addRow('Function', self.filterfunction)
        formlayout.addRow('Cut off', self.filtercutoff)
        formlayout.addRow('Bandwidth', self.filterbandwidth)
        formlayout.addRow('Order', self.filterorder)

        filterbox = QGroupBox('Filter')
        filterbox.setLayout(formlayout)

        options = QDockWidget('Options', self)
        options.setFeatures(QDockWidget.DockWidgetFloatable)
        options.setFeatures(QDockWidget.DockWidgetMovable)
        options.setWidget(filterbox)

        self.mselabel = QLabel('No image selected')

        infoform = QFormLayout()
        infoform.addRow('MSE:', self.mselabel)

        imagebox = QGroupBox('Image')
        imagebox.setLayout(infoform)

        information = QDockWidget('Information', self)
        information.setFeatures(QDockWidget.DockWidgetFloatable)
        information.setFeatures(QDockWidget.DockWidgetMovable)
        information.setWidget(imagebox)

        self.addDockWidget(Qt.RightDockWidgetArea, options)
        self.addDockWidget(Qt.RightDockWidgetArea, information)

    def initcentralwidget(self):
        mainlayout = QGridLayout()
        mainlayout.addWidget(self.originalimage_box, 0, 0, 2, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_magnitude_box, 0, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_phase_box, 0, 3, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_realpart_box, 1, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_imaginarypart_box, 1, 3, Qt.AlignCenter)

        mainlayout.addWidget(self.reconstructedimage_box, 2, 0, 2, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_magnitude_box, 2, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_phase_box, 2, 3, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_realpart_box, 3, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_imaginarypart_box, 3, 3, Qt.AlignCenter)

        centralwidget = QWidget()
        centralwidget.setLayout(mainlayout)
        return centralwidget

    def filtercutofflistener(self, value):
        self.processor.filter_cutoff = value
        self.processor.apply()
        self.updateimages()

    def filterbandwidthlistener(self, value):
        self.processor.band_width = value
        self.processor.apply()
        self.updateimages()

    def filterorderlistener(self, value):
        print('Order', value)

    def filtertypelistener(self, index):
        print('Type', index)
        if index == self._type_none:
            self.filterfunction.setEnabled(False)
            self.filterfunction.setCurrentIndex(0)
            self.filtercutoff.setEnabled(False)
            self.filtercutoff.setValue(0.0)
            self.filterbandwidth.setEnabled(False)
            self.filterbandwidth.setValue(0.0)
            self.filterorder.setEnabled(False)
            self.filterorder.setValue(1.0)
        else:
            self.filterfunction.setEnabled(True)
            self.filtercutoff.setEnabled(True)
            self.filterbandwidth.setEnabled(True)

        typemap = [
            None,
            'lowpass',
            'highpass',
            'bandreject',
            'bandpass'
        ]

        self.processor.filter_type = typemap[index]
        self.processor.apply()
        self.updateimages()

    def filterfunctionlistener(self, index):
        print('Function', index)
        self.filterorder.setEnabled(index == self._function_butterworth)
        if index != self._function_butterworth:
            self.filterorder.setValue(1.0)

        funcmap = [
            'ideal',
            'butterworth',
            'gauss'
        ]

        self.processor.filter_function = funcmap[index]
        self.processor.apply()
        self.updateimages()

    def opendialog(self, path):
        filepath = QFileDialog.getOpenFileName(self, 'Open file', path)
        if filepath[0] != '':
            self.processor.original = Image.from_file(filepath[0])
            self.processor.apply()
            self.updateimages()

    def closeEvent(self,event):
        reply = QMessageBox.question(
            self,
            'Message',
            "Are you Sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def run_app(argv):
    app = QApplication(argv)
    mainwindow = MainWindow(app)
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app(sys.argv)
