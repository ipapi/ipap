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
        originalimage = self.processor.original
        originalpixelmap = QPixmap.fromImage(make_qimage(originalimage))

        # Images
        imageoriginal = QLabel("Original")
        imageoriginal.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        imageoriginal.setPixmap(originalpixelmap)

        imagereconstructed = QLabel("Reconstructed")
        imagereconstructed.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        imagemagnitude = QLabel("Magnitude")
        imagemagnitude.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        imagerealpart = QLabel("Real part")
        imagerealpart.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        imageimaginarypart = QLabel("Imaginary part")
        imageimaginarypart.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        mainlayout = QGridLayout()
        mainlayout.addWidget(imageoriginal, 0, 0, Qt.AlignCenter)
        mainlayout.addWidget(imagereconstructed, 1, 0, Qt.AlignCenter)

        mainlayout.addWidget(imagemagnitude, 0, 1, 1, 2, Qt.AlignCenter)
        mainlayout.addWidget(imagerealpart, 1, 1, Qt.AlignCenter)
        mainlayout.addWidget(imageimaginarypart, 1, 2, Qt.AlignCenter)

        mainwidget = QWidget()
        mainwidget.setLayout(mainlayout)

        self.setCentralWidget(mainwidget)
        self.statusBar()

        self.initoptionspanel()
        self.initmenubar()

        self.setGeometry(100, 100, 1080, 720)
        self.setWindowTitle("Ipap")

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

        filterfunction = QComboBox()
        filterfunction.addItem('None')
        filterfunction.addItem('Charlie')
        filterfunction.addItem('Delta')
        filterfunction.addItem('Echo')
        filterfunction.currentIndexChanged.connect(self.filterfunctionlistener)

        doublevalidator = QDoubleValidator()

        filtercutoff = QLineEdit()
        filtercutoff.setText('0')
        filtercutoff.setValidator(doublevalidator)
        filtercutoff.textChanged.connect(self.filtercutofflistener)

        filterbandwidth = QLineEdit()
        filterbandwidth.setText('0')
        filterbandwidth.setValidator(doublevalidator)
        filterbandwidth.textChanged.connect(self.filterbandwidthlistener)

        self.filterorder = QLineEdit()
        self.filterorder.setText('1')
        self.filterorder.setValidator(doublevalidator)
        self.filterorder.textChanged.connect(self.filterorderlistener)
        self.filterorder.setEnabled(False)

        formlayout = QFormLayout()
        formlayout.addRow('Type', filtertype)
        formlayout.addRow('Function', filterfunction)
        formlayout.addRow('Cut off', filtercutoff)
        formlayout.addRow('Bandwidth', filterbandwidth)
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

    def filtercutofflistener(self, value):
        print('cutoff', value)

    def filterbandwidthlistener(self, value):
        print('Bandwidth', value)

    def filterorderlistener(self, value):
        print('Order', value)

    def filtertypelistener(self, index):
        print('Type', index)

    def filterfunctionlistener(self, index):
        print('Function', index)
        self.filterorder.setEnabled(index == 1)

    def showdialog(self):
        fname = QFileDialog.getOpenFileName(self,'Open file', '/Users/Thomas')

        if fname[0]:
            f = open(fname[0], encoding="utf8")
            with f:
                data = f.read()
                self.textEdit.setText(data)

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
