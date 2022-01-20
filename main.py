
import sqlite3
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtUiTools import QUiLoader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("untitled.ui")
        self.ui.show()
        ####database
        self.conn = sqlite3.connect("database.db")
        self.my_curor = self.conn.cursor()
        self.load_date()
        self.ui.addButton.clicked.connect(self.add_contact)
        self.ui.removeButton_2.clicked.connect(self.remove_all)
        self.ui.removeButton.clicked.connect(self.remove_contact)
        self.ui.darkmode.clicked.connect(self.darkmode)
        self.i = 0
        self.LAST_ID = 0

    def add_contact(self):
        self.my_curor.execute("SELECT ID FROM People")
        ID = self.my_curor.fetchall()

        try:
            self.i = ID[-1][0]
        except:
            pass
        self.i+=1
        print(self.i)
        name = str(self.ui.textEdit.toPlainText())
        last = str(self.ui.textEdit_2.toPlainText())
        phone = str(self.ui.textEdit_3.toPlainText())
        email = str(self.ui.textEdit_4.toPlainText())

        if len(name) != 0 and len(last) != 0 and len(phone) != 0 and len(email) != 0:
            self.my_curor.execute(f"INSERT INTO People VALUES ('{self.i}','{name}','{last}','{phone}','{email}')")
            label = QLabel()
            label.setText(
            name + "             " + last + "            " + phone + "        " + email)
            self.ui.verticalLayout.addWidget(label)
            self.lastRecord = label
            self.conn.commit()
        else:
            pass



    def darkmode(self):
        if self.ui.darkmode.isChecked():
            self.ui.setStyleSheet("background-color: rgb(83, 83, 83);")
            self.ui.label.setStyleSheet("background-color: rgb(144, 144, 144);")
        else:
            self.ui.setStyleSheet("background-color: rgb(225, 225, 225);")
            self.ui.label.setStyleSheet("background-color: rgb(255, 255, 255);")

    def remove_contact(self):
        self.my_curor.execute("SELECT ID FROM People")
        ID = self.my_curor.fetchall()
        try:
            self.LAST_ID = ID[-1][0]
        except:
            pass
        print(self.LAST_ID)
        self.my_curor.execute(f"DELETE FROM People WHERE ID={self.LAST_ID}")
        self.conn.commit()
        self.lastRecord.setText("")
        self.ui.verticalLayout.addWidget(self.lastRecord)
        self.LAST_ID -= 1
        self.updater()
    def remove_all(self):
        self.my_curor.execute("DELETE FROM People")
        self.conn.commit()
        for i in reversed(range( self.ui.verticalLayout.count())):
            self.ui.verticalLayout.itemAt(i).widget().deleteLater()


    def load_date(self):
        self.ui.verticalLayout.setAlignment(Qt.AlignTop)
        try:
            self.my_curor.execute("SELECT * FROM people")
            result = self.my_curor.fetchall()

            for item in result:
                label = QLabel()
                label.setText(str(item[1])+"             " +str(item[2]) +"            "+ str(item[3])+"        "+str(item[4]))
                self.ui.verticalLayout.addWidget(label)
                self.lastRecord = label
        except:
            pass

    def updater(self):

        for i in reversed(range( self.ui.verticalLayout.count())):
            self.ui.verticalLayout.itemAt(i).widget().deleteLater()

        self.my_curor.execute("SELECT * FROM people")
        result = self.my_curor.fetchall()

        for item in result:
            label = QLabel()
            label.setText(
                str(item[1]) + "             " + str(item[2]) + "            " + str(item[3]) + "        " + str(
                    item[4]))
            self.ui.verticalLayout.addWidget(label)
            self.lastRecord = label



if __name__ == "__main__":
    app = QApplication()
    cal = MainWindow()
    app.exec()