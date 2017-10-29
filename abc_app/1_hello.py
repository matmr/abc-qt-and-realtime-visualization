import sys

from PyQt5 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""
    def __init__(self):
        super().__init__()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())