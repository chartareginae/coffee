import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog

d = ()


class EmployeeDlg(QDialog):
    def __init__(self, parent=None, new_coffee=False):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.buttonBox.clicked.connect(self.get_values)
        self.new_coffee = new_coffee
        if self.new_coffee:
            self.lineEdit.hide()
            self.label_7.hide()

    def get_values(self):
        global d
        if self.new_coffee:
            d = (self.variety.text(), self.degree_of_roasting.text(), self.ground_or_not.text(),
                 self.describtion_of_taste.text(), self.price.text(), self.volume.text())
        else:
            d = (self.variety.text(), self.degree_of_roasting.text(), self.ground_or_not.text(),
                 self.describtion_of_taste.text(), self.price.text(), self.volume.text(), int(self.lineEdit.text()))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('espresso.ui', self)
        self.secondW = None
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.loadTable()
        self.add_coffee.clicked.connect(self.add_coffeee)
        self.replace_coffee.clicked.connect(self.rename)

    def loadTable(self):
        exer = self.cur.execute('SELECT * FROM coffee1')
        ti = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
              'объем упаковки']
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

    def add_coffeee(self):
        global d
        dlg = EmployeeDlg(self, new_coffee=True)
        dlg.exec_()
        id = [int(self.cur.execute("SELECT max(id) FROM coffee1").fetchone()[0]) + 1]
        id.extend(list(d))
        self.cur.execute('INSERT INTO coffee1 VALUES(?,?,?,?,?,?,?)', id)
        self.con.commit()
        self.loadTable()

    def rename(self):
        global d
        dlg = EmployeeDlg(self, new_coffee=False)
        dlg.exec_()
        print(d)
        self.cur.execute(f'''UPDATE coffee1 SET name = "{d[0]}", stepen = "{d[1]}", molotyy = "{d[2]}", vkus = "{d[3]}",
                             price = "{d[4]}", value = "{d[5]}" WHERE id = {d[6]}''')
        self.con.commit()
        self.loadTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())