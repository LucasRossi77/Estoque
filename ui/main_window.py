from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel
)

from PyQt6.QtGui import QColor, QPixmap
from services.item_service import listar_itens
from ui.add_item_window import AddItemWindow
from utils.alertas import estoque_baixo


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Estoque TI")
        self.resize(900, 600)

        # WIDGET CENTRAL
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # LAYOUT PRINCIPAL
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # BARRA SUPERIOR
        barra = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Pesquisar item...")
        self.search.textChanged.connect(self.filtrar_itens)

        btn_add = QPushButton("Adicionar Item")
        btn_add.clicked.connect(self.abrir_add_item)

        barra.addWidget(self.search)
        barra.addWidget(btn_add)

        layout.addLayout(barra)

        # TABELA
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Foto",
            "Nome",
            "Caixa",
            "Localização",
            "Quantidade",
            "Min"
        ])

        layout.addWidget(self.table)

        # CARREGAR ITENS
        self.carregar_itens()

    def carregar_itens(self):

        itens = listar_itens()

        self.table.setRowCount(len(itens))

        for row, item in enumerate(itens):

            # FOTO
            if item["foto"]:
                label = QLabel()

                pixmap = QPixmap(item["foto"])
                pixmap = pixmap.scaled(50, 50)

                label.setPixmap(pixmap)

                self.table.setCellWidget(row, 0, label)

            # NOME
            self.table.setItem(row, 1, QTableWidgetItem(item["nome"]))

            # CAIXA
            self.table.setItem(row, 2, QTableWidgetItem(str(item["caixa"])))

            # LOCALIZAÇÃO
            self.table.setItem(row, 3, QTableWidgetItem(str(item["localizacao"])))

            # QUANTIDADE
            self.table.setItem(row, 4, QTableWidgetItem(str(item["quantidade"])))

            # QUANTIDADE MINIMA
            self.table.setItem(row, 5, QTableWidgetItem(str(item["quantidade_minima"])))

            # ALERTA ESTOQUE BAIXO
            if estoque_baixo(item["quantidade"], item["quantidade_minima"]):

                for col in range(6):
                    cell = self.table.item(row, col)

                    if cell:
                        cell.setBackground(QColor(255,150,150))

    def filtrar_itens(self):

        texto = self.search.text().lower()

        for row in range(self.table.rowCount()):

            item = self.table.item(row, 1)

            if item:
                nome = item.text().lower()
                self.table.setRowHidden(row, texto not in nome)

    def abrir_add_item(self):

        self.add_window = AddItemWindow(self.recarregar_tabela)
        self.add_window.show()

    def recarregar_tabela(self):

        self.table.setRowCount(0)
        self.carregar_itens()