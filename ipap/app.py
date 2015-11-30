import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("ipap")


def run_app(argv):
    app = QApplication(argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app(sys.argv)
