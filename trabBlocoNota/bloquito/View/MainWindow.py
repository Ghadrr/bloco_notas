import sqlite3
import sys

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QWidget, QTableWidget, QPushButton, QVBoxLayout, QMainWindow, QLineEdit, QTextEdit, \
    QDialog, QApplication, QSizePolicy, QLabel, QComboBox, QMessageBox, QGridLayout, QTableWidgetItem, QAbstractItemView
from bloquito.Controller.bloco_dao import DataBase
from bloquito.Model.bloco import Nota

db = DataBase()
db.connect()
db.create_table_notas()
db.close_connection()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(400, 700)

        self.setWindowTitle('Cadastro de Cliente')

        self.lbl_id = QLabel('id')
        self.txt_id = QLineEdit()
        self.txt_id.setReadOnly(True)
        self.lbl_note_title = QLabel('Título da Nota')
        self.txt_note_title = QLineEdit()
        self.lbl_nota = QLabel('Nota')
        self.txt_nota = QTextEdit()

        self.btn_salvar = QPushButton('Salvar')
        self.btn_ver_notas = QPushButton('Exibir Notas')
        self.btn_remover = QPushButton('Remover')

        self.qtw_notas = QTableWidget()
        self.qtw_notas.setColumnCount(4)
        self.qtw_notas.setHorizontalHeaderLabels(['ID', 'TÍTULO', 'NOTA', 'DATA'])
        self.qtw_notas.setSelectionMode(QAbstractItemView.NoSelection)
        self.qtw_notas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.qtw_notas.cellDoubleClicked.connect(self.popular_nota)

        layout = QVBoxLayout()

        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_note_title)
        layout.addWidget(self.txt_note_title)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)

        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_remover)

        layout.addWidget(self.qtw_notas)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_remover.clicked.connect(self.deletar)
        self.ler_notas()

    def ler_notas(self):
        self.qtw_notas.setRowCount(0)
        db = DataBase()
        db.connect()
        notas = db.ler_notas()
        self.qtw_notas.setRowCount(len(notas))
        for linha, nota in enumerate(notas):
            for coluna, valor in enumerate(nota):
                self.qtw_notas.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def popular_nota(self, row, column):
        self.txt_id.setText(self.qtw_notas.item(row, 0).text())
        self.txt_note_title.setText(self.qtw_notas.item(row, 1).text())
        self.txt_nota.setText(self.qtw_notas.item(row, 2).text())
        self.btn_salvar.setText("Atualizar")

    def deletar(self):
        db = DataBase()
        try:
            db.excluir_nota(int(self.txt_id.text()))
            self.ler_notas()
            self.limpar()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('ERROR')
            msg.setText('SELECIONE ALGO PARA REMOVER')
            msg.exec()
        finally:
            self.btn_salvar.setText("Salvar")

    def salvar_nota(self):

        if not self.campos_vazios():
            db = DataBase()

            nota = Nota(
                id=self.txt_id.text(),
                titulo=self.txt_note_title.text(),
                texto=self.txt_nota.toPlainText()
            )
            if self.btn_salvar.text() == "Salvar":
                retorno = db.registrar_nota(nota)
                if retorno == 'Ok':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle('SALVO')
                    msg.setText('NOTA SALVA COM SUCESSO')
                    msg.exec()
                    self.limpar()
                    self.ler_notas()
            elif self.btn_salvar.text() == 'Atualizar':
                retorno = db.atualizar_nota(nota)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('NOTA ATUALIZADA')
                msg.setText(f'A NOTA FOI ATUALIZADA')
                self.btn_salvar.setText("Salvar")
                self.limpar()
                msg.exec()
                self.ler_notas()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('ERRO AO SALVAR')
            msg.setText(f'ERRO AO SALVAR A NOTA')
            msg.exec()

    def limpar(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
                self.txt_nota.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

    def campos_vazios(self):
        return self.txt_note_title.text() == '' \
            or self.txt_nota.toPlainText() == ''
