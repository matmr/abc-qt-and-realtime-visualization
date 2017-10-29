import sys

import time

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
        self.coin_name_input = QtWidgets.QLineEdit()
        self.coin_amount_input = QtWidgets.QDoubleSpinBox()
        self.coin_buy_price_input = QtWidgets.QDoubleSpinBox()
        self.coin_exchange = QtWidgets.QComboBox()
        self.coin_exchange.addItems(
            ['Poloniex', 'Bittrex', 'Bitstamp', 'Kraken']
        )

        self.coin_add_button = QtWidgets.QPushButton('Add')
 

        layout_coin = QtWidgets.QFormLayout()
        layout_coin.addRow('Coin', self.coin_name_input)
        layout_coin.addRow('Amount', self.coin_amount_input)
        layout_coin.addRow('Exchange', self.coin_exchange)
        layout_coin.addRow('Price/coin', self.coin_buy_price_input)

        layout_coin_line = QtWidgets.QHBoxLayout()
        layout_coin_line.addLayout(layout_coin)

        self.layout.addLayout(layout_coin_line)
        self.layout.addWidget(self.coin_add_button)

        self.coin_add_button.clicked.connect(lambda: time.sleep(3))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = CryptoShill()
    main.show()

    sys.exit(app.exec_())