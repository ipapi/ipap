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

from PyQt5.QtCore import Qt
from PyQt5.Qt import QDoubleValidator
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


def make_dft_mag_qimage(image):
    imageformat = QImage.Format_RGBA8888
    imagedata = image.dft_magnitude
    # print(imagedata)
    print(imagedata.flatten())
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    return qimage


def make_dft_real_qimage(image):
    imageformat = QImage.Format_Indexed8
    imagedata = image.dft_real
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    qimage.setColorTable(grayscale_colortable())
    return qimage


def make_dft_imag_qimage(image):
    imageformat = QImage.Format_Indexed8
    imagedata = image.dft_imag
    qimage = QImage(imagedata.flatten(),
                    imagedata.shape[1],
                    imagedata.shape[0],
                    imageformat)
    qimage.setColorTable(grayscale_colortable())
    return qimage


class MainWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self._app = app

        self.processor = ImageProcessor()
        self.processor.original = Image.from_file('lena.png')

        # self.processor.filter_type = 'lowpass'
        # self.processor.filter_function = 'ideal'
        self.processor.apply()
        self.initui()

    def initui(self):
        self.initmenubar()
        self.initoptionspanel()
        self.initlabels()
        self.updateimages()
        centralwidget = self.initcentralwidget()
        self.setCentralWidget(centralwidget)
        self.statusBar()
        self.setGeometry(100, 100, 1080, 720)
        self.setWindowTitle("Ipap")

    def initlabels(self):
        # Initialize image containers
        self.originalimage_container = QLabel('Original Image Placeholder')
        self.originalimage_magnitude_container = QLabel('Original Magnitude Placeholder')
        self.originalimage_realpart_container = QLabel('Original Real Part Placeholder')
        self.originalimage_imaginarypart_container = QLabel('Original Imaginary Part Placeholder')
        self.originalimage_phase_container = QLabel('Original Phase Placeholder')
        self.reconstructedimage_container = QLabel('Reconstructed Image Placeholder')
        self.reconstructedimage_magnitude_container = QLabel('Reconstructed Magnitude Placeholder')
        self.reconstructedimage_realpart_container = QLabel('Reconstructed Imaginary Part Placeholder')
        self.reconstructedimage_imaginarypart_container = QLabel('Reconstructed Real Part Placeholder')
        self.reconstructedimage_phase_container = QLabel('Reconstructed Phase Placeholder')

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
        originalimage = self.processor.original
        self.originalimage_container.setPixmap(QPixmap.fromImage(make_qimage(originalimage)))

    def initmenubar(self):
        opennewfile = QAction('Open File', self)
        opennewfile.setShortcut('Ctrl+O')
        opennewfile.setStatusTip('Open File')
        opennewfile.triggered.connect(self.showdialog)

        opendbfile = QAction('Open from DB', self)
        opendbfile.setShortcut('Ctrl+Shift+O')
        opendbfile.setStatusTip('Open file from database')

        exitprogram = QAction('Quit', self)
        exitprogram.setShortcut('Ctrl+Q')
        exitprogram.setStatusTip('Exit the application')
        exitprogram.triggered.connect(self._app.closeAllWindows)

        menufile = self.menuBar().addMenu('File')
        menufile.addAction(opennewfile)
        menufile.addAction(opendbfile)
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

        doublevalidator = QDoubleValidator()

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

        equallabel = QLabel('No image selected')

        infoform = QFormLayout()
        infoform.addRow('Equal:', equallabel)

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
        mainlayout.addWidget(self.originalimage_box, 0, 0, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_magnitude_box, 0, 1, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_realpart_box, 0, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_imaginarypart_box, 0, 3, Qt.AlignCenter)
        mainlayout.addWidget(self.originalimage_phase_box, 0, 4, Qt.AlignCenter)

        mainlayout.addWidget(self.reconstructedimage_box, 1, 0, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_magnitude_box, 1, 1, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_realpart_box, 1, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_imaginarypart_box, 1, 3, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_phase_box, 1, 4, Qt.AlignCenter)

        centralwidget = QWidget()
        centralwidget.setLayout(mainlayout)
        return centralwidget

    def filtercutofflistener(self, value):
        print('cutoff', value)

    def filterbandwidthlistener(self, value):
        print('Bandwidth', value)

    def filterorderlistener(self, value):
        print('Order', value)

    def filtertypelistener(self, index):
        print('Type', index)
        if index == 0:
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

    def filterfunctionlistener(self, index):
        print('Function', index)
        self.filterorder.setEnabled(index == 2)
        if index != 2:
            self.filterorder.setValue(1.0)

    def showdialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')

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
