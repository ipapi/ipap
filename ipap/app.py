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
    QDockWidget
)

from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self._rawdata_app = app
        self.initUI()

    def initUI(self):

        self.progressBar = QProgressBar()
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        text = QTextEdit();
        dock = QDockWidget("Dock", self)
        dock.setFeatures(QDockWidget.DockWidgetFloatable)
        dock.setFeatures(QDockWidget.DockWidgetMovable)
        dock.setWidget(text)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        opennewfile = QAction('Open File', self)
        opennewfile.setShortcut('Ctrl+O')
        opennewfile.setStatusTip('Open File')
        opennewfile.triggered.connect(self.showDialog)

        opendbfile = QAction('Open from DB', self)
        opendbfile.setShortcut('Ctrl+Shift+O')
        opendbfile.setStatusTip('Open file from database')

        exitprogram = QAction('Quit', self)
        exitprogram.setShortcut('Ctrl+Q')
        exitprogram.setStatusTip('Exit the application')
        exitprogram.triggered.connect(self._rawdata_app.closeAllWindows)

        menufile = self.menuBar().addMenu('File')
        menufile.addAction(opennewfile)
        menufile.addAction(opendbfile)
        menufile.addAction(exitprogram)

        self.setGeometry(300, 300, 1080, 720)
        self.setWindowTitle("Ipap")

    def showDialog(self):

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
