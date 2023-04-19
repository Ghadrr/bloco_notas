import sqlite3
from bloquito.Model.bloco import Nota


import sqlite3
from PySide6.QtGui import QStandardItemModel, QStandardItem




class DataBase:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect('notas.db')

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_table_notas(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS NOTAS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TITULO TEXT,
            TEXTO TEXT,
            DATA TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.connection.commit()
        self.close_connection()

    def registrar_nota(self, nota):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO NOTAS (TITULO, TEXTO) VALUES (?, ?)""",
                (nota.titulo, nota.texto)
            )
            self.connection.commit()
            self.close_connection()
            return 'Ok'
        except sqlite3.Error as e:
            return str(e)

    def ler_notas(self):

        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM NOTAS""")
        notas = cursor.fetchall()
        self.close_connection()
        return notas

    def atualizar_nota(self, nota):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """UPDATE NOTAS SET TITULO=?, TEXTO=? WHERE ID=?""",
                (nota.titulo, nota.texto, nota.id)
            )
            self.connection.commit()
            self.close_connection()
            return 'Ok'
        except sqlite3.Error as e:
            return str(e)

    def excluir_nota(self, nota_id):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute("""DELETE FROM NOTAS WHERE ID=?""", (nota_id,))
            self.connection.commit()
            self.close_connection()
            return 'Ok'
        except sqlite3.Error as e:
            return str(e)