from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, 
    QTableWidgetItem, QLabel, QHeaderView
)
from PyQt6.QtCore import Qt
from services.movimentacao_service import listar_historico

class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relatórios de Movimentação")
        self.resize(800, 500)
        self.setStyleSheet("background-color: #e8e0cc;")

        layout = QVBoxLayout()

        titulo = QLabel("Histórico de Movimentação")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Tabela de Relatórios
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Item", "Qtd", "Caminho", "Responsável", "Data", "Observação"
        ])
        
        # Ajusta as colunas para ocuparem o espaço disponível
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.carregar_dados()

    def carregar_dados(self):
        dados = listar_historico()
        self.table.setRowCount(len(dados))

        for row, mov in enumerate(dados):
            # Formatando a data (pegando apenas os caracteres principais)
            data_formatada = str(mov["data"])[:19]
            
            self.table.setItem(row, 0, QTableWidgetItem(mov["item_nome"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(mov["quantidade"])))
            self.table.setItem(row, 2, QTableWidgetItem(mov["tipo"]))
            self.table.setItem(row, 3, QTableWidgetItem(mov["usuario_nome"] or "Registro Antigo (Sem Usuário)"))
            self.table.setItem(row, 4, QTableWidgetItem(data_formatada))
            self.table.setItem(row, 5, QTableWidgetItem(mov["observacao"] or "-"))

            # Cores para diferenciar Entrada de Saída
            cor = Qt.GlobalColor.green if mov["tipo"] == "ENTRADA" else Qt.GlobalColor.red
            self.table.item(row, 2).setForeground(cor)