import sys

import pandas as pd

from PyQt5 import QtWidgets, QtCore


_COLUMNS = [
    'Altcoin',
    'Amount',
    'Exchange',
    'Price'
]

class CryptoShill(QtWidgets.QMainWindow):
    """Main window of the application."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Crypto Shill')
        self.setMinimumSize(500, 700)

        main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(main_widget)

        self.layout = QtWidgets.QVBoxLayout()

        self.set_up_gui()
        self.set_up_signals_and_slots()

        main_widget.setLayout(self.layout)


    def set_up_gui(self):
        """Take care of all widgets and layouts."""
        menu_bar = self.menuBar()

        action_open = QtWidgets.QAction('&Open', self)
        action_save = QtWidgets.QAction('&Save', self)
        action_save.triggered.connect(self.save_file)
        action_exit = QtWidgets.QAction('&Exit', self)
        action_exit.triggered.connect(self.close)

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(action_open)
        file_menu.addAction(action_save)
        file_menu.addAction(action_exit)

        self.coin_name_input = QtWidgets.QLineEdit()

        self.coin_exchange = QtWidgets.QComboBox()
        self.coin_exchange.addItems(
            ['Poloniex', 'Bittrex', 'Bitstamp', 'Kraken']
        )

        self.coin_amount_input = QtWidgets.QDoubleSpinBox()
        self.coin_amount_input.setRange(0.0, 1e6)
        self.coin_amount_input.setDecimals(4)
        self.coin_amount_input.setSingleStep(0.1)

        self.coin_buy_price_input = QtWidgets.QDoubleSpinBox()
        self.coin_buy_price_input.setRange(0.0, 1e6)
        self.coin_buy_price_input.setDecimals(4)
        self.coin_buy_price_input.setSingleStep(0.1)

        self.coin_add_button = QtWidgets.QPushButton('Add Coin to Portfolio')

        self.coin_table = QtWidgets.QTableView()
        self.coin_table_model = TableModel(self)
        self.coin_table.setModel(self.coin_table_model)
        self.coin_table.setAlternatingRowColors(True)
        self.coin_table.setSortingEnabled(True)
        hh = self.coin_table.horizontalHeader()
        hh.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        layout_coin = QtWidgets.QFormLayout()
        layout_coin.addRow('Coin', self.coin_name_input)
        layout_coin.addRow('Amount', self.coin_amount_input)
        layout_coin.addRow('Exchange', self.coin_exchange)
        layout_coin.addRow('Price/coin', self.coin_buy_price_input)
        
        self.layout.addLayout(layout_coin)
        self.layout.addWidget(self.coin_add_button)
        self.layout.addWidget(self.coin_table)

    def set_up_signals_and_slots(self):
        """Take care of all actions."""
        def new_table_entry():
            entry = [
                self.coin_name_input.text(),
                self.coin_amount_input.value(),
                self.coin_exchange.currentText(),
                self.coin_buy_price_input.value()
            ]

            self.coin_table_model.update(entry)

        self.coin_add_button.clicked.connect(new_table_entry)


    def save_file(self):
        """Open Save as ... dialogue."""
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self, self.tr('Save file as'), '/.', self.tr('.shill')
        )[0]

        self.coin_table_model.datatable.to_pickle(file_name)



class TableModel(QtCore.QAbstractTableModel):
    '''Table model that suits all tables (for now). It specifies
    access to data and some other stuff.'''
    def __init__(self, parent, *args):
        super(TableModel, self).__init__(parent, *args)
        self.datatable = pd.DataFrame(columns=_COLUMNS)

    def update(self, data):
        self.layoutAboutToBeChanged.emit()

        self.datatable = pd.concat(
            [self.datatable, pd.DataFrame([data], columns=_COLUMNS)]
        )
        self.datatable.columns = _COLUMNS

        self.layoutChanged.emit()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.datatable.index.size

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.datatable.columns.values.size

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.datatable.columns[col]
        return None

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None

        i = index.row()
        j = index.column()

        return str(self.datatable.iat[i, j])

    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()
        if order == QtCore.Qt.DescendingOrder:
            self.datatable = self.datatable.sort_values(by=self.datatable.columns[col], ascending=0)
        else:
            self.datatable = self.datatable.sort_values(by=self.datatable.columns[col])
        self.layoutChanged.emit()

    def flags(self, index):
        return QtCore.QAbstractTableModel.flags(self, index)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = CryptoShill()
    main.show()

    sys.exit(app.exec_())