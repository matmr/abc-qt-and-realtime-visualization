import sys

from PyQt5 import QtWidgets, QtCore


class CryptoShill(QtWidgets.QMainWindow):
    """Main window of the application."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Crypto Shill')
        self.setMinimumSize(600, 400)

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.set_up_gui()


    def set_up_gui(self):
        """Takes care of all widgets and layouts."""
        self.label = QtWidgets.QLabel('Input your coin and amount:')
        self.coin_name_input = QtWidgets.QLineEdit()
        self.coin_amount_input = QtWidgets.QDoubleSpinBox()
        self.coin_buy_price_input = QtWidgets.QDoubleSpinBox()
        self.coin_exchange = QtWidgets.QComboBox()
        self.coin_exchange.addItems(
            ['Poloniex', 'Bittrex', 'Bitstamp', 'Kraken']
        )

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.coin_name_input)
        self.layout.addWidget(self.coin_amount_input)
        self.layout.addWidget(self.coin_exchange)
        self.layout.addWidget(self.coin_buy_price_input)






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = CryptoShill()
    main.show()

    sys.exit(app.exec_())