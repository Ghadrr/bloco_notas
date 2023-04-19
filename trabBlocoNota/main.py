import sys
from PySide6.QtCore import Qt, QModelIndex, QDateTime
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QTextEdit, QDialog

from bloquito.Controller.bloco_dao import DataBase
from bloquito.View.MainWindow import MainWindow

db = DataBase()
db.connect()
db.create_table_notas()
db.close_connection()


args = sys.argv

app = QApplication(sys.argv)
principal = MainWindow()
principal.show()
app.exec()