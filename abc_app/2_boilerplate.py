import sys

from PyQt5 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Hello!')
        self.setMinimumSize(600, 400)


        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.layout)

    def set_up_gui(self):
        """..."""
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())