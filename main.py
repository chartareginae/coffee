import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('espresso.ui', self)

        self.loadTable('coffee')


    def loadTable(self, table_name):
        con = sqlite3.connect(table_name)
        cur = con.cursor()
        exer = cur.execute('SELECT * FROM coffee1')
        ti = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки']
        self.tableWidget.setColumnCount(len(ti))
        self.tableWidget.setHorizontalHeaderLabels(ti)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(exer):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())