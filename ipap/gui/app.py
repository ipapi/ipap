import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMessageBox,
    QAction,
    QFileDialog,
    QMainWindow,
    QTextEdit,
    QProgressBar,
    QStatusBar,
    QDockWidget,
    QFormLayout,
    QGroupBox,
    QComboBox,
    QLabel,
    QLineEdit
)

from PyQt5.QtCore import Qt
from PyQt5.Qt import QDoubleValidator

class MainWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self._app = app
        self.initui()

    def initui(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
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

        groupbox = QGroupBox('Filter')
        groupbox.setLayout(formlayout)

        dock = QDockWidget('Options', self)
        dock.setFeatures(QDockWidget.DockWidgetFloatable)
        dock.setFeatures(QDockWidget.DockWidgetMovable)
        dock.setWidget(groupbox)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

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
        fname = QFileDialog.getOpenFileName(self,'Open file', '/home')

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
