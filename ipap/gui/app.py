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
    QFrame
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
        self.originalimage_label = QLabel('Original Image')
        self.originalimage_label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.reconstructedimage_label = QLabel("Reconstructed Image")
        self.reconstructedimage_label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.magnitudeimage_label = QLabel("Magnitude Image")
        self.magnitudeimage_label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.realpartimage_label = QLabel("Real Part Image")
        self.realpartimage_label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.imaginarypartimage_label = QLabel("Imaginary Part Image")
        self.imaginarypartimage_label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

    def updateimages(self):
        originalimage = self.processor.original
        self.originalimage_label.setPixmap(QPixmap.fromImage(make_qimage(originalimage)))

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
        filtertype.addItem('Alpha')
        filtertype.addItem('Bravo')
        filtertype.currentIndexChanged.connect(self.filtertypelistener)

        self.filterfunction = QComboBox()
        self.filterfunction.addItem('Charlie')
        self.filterfunction.addItem('Delta')
        self.filterfunction.addItem('Butterworth')
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
        mainlayout.addWidget(self.originalimage_label, 0, 0, Qt.AlignCenter)
        mainlayout.addWidget(self.reconstructedimage_label, 1, 0, Qt.AlignCenter)
        mainlayout.addWidget(self.magnitudeimage_label, 0, 1, 1, 2, Qt.AlignCenter)
        mainlayout.addWidget(self.realpartimage_label, 1, 1, Qt.AlignCenter)
        mainlayout.addWidget(self.imaginarypartimage_label, 1, 2, Qt.AlignCenter)
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
