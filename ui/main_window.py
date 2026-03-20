from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
    QAbstractItemView, QInputDialog, QMessageBox
)
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtCore import Qt 

from ui.reports_window import ReportsWindow
from services.item_service import listar_itens, atualizar_quantidade
from ui.add_item_window import AddItemWindow
from utils.alertas import estoque_baixo
from services.movimentacao_service import registrar_movimentacao

class MainWindow(QMainWindow):

    def __init__(self, usuario_id=None):
        super().__init__()
        self.usuario_id = usuario_id

        self.setWindowTitle("Estoque TI")
        self.resize(900, 600)

        # WIDGET CENTRAL E LAYOUTS
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # BARRA SUPERIOR
        barra = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Pesquisar item...")
        self.search.textChanged.connect(self.filtrar_itens)

        btn_relatorios = QPushButton("Ver Relatórios")
        btn_relatorios.clicked.connect(self.abrir_relatorios)
        
        

        btn_add = QPushButton("Adicionar Item")
        btn_add.clicked.connect(self.abrir_add_item)

        barra.addWidget(self.search)
        barra.addWidget(btn_add)
        barra.addWidget(btn_relatorios) # Adiciona o novo botão

        barra.addWidget(self.search)
        barra.addWidget(btn_add)
        layout.addLayout(barra)

        # TABELA
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Foto", "Nome", "Caixa", "Localização", "Quantidade", "Min"
        ])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.abrir_menu_item)
        layout.addWidget(self.table)

        self.carregar_itens()

    def carregar_itens(self):
        itens = listar_itens()
        self.table.setRowCount(len(itens))

        for row, item in enumerate(itens):
            self.table.setRowHeight(row, 60)

            # FOTO
            if item["foto"]:
                label = QLabel()
                pixmap = QPixmap(item["foto"])
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
                    label.setPixmap(pixmap)
                self.table.setCellWidget(row, 0, label)
            else:
                self.table.setItem(row, 0, QTableWidgetItem("Sem foto"))

            # NOME + ID
            nome_item = QTableWidgetItem(item["nome"])
            # <-- CORREÇÃO: Puxar como id_item, conforme criado no create_tables.py
            nome_item.setData(Qt.ItemDataRole.UserRole, item["id_item"])   
            self.table.setItem(row, 1, nome_item)

            # DADOS RESTANTES
            self.table.setItem(row, 2, QTableWidgetItem(str(item["caixa"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item["localizacao"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(item["quantidade"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(item["quantidade_minima"])))

            # ALERTA
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

    def abrir_menu_item(self, row, column):
        nome_item = self.table.item(row, 1).text()
        item_id = self.table.item(row, 1).data(Qt.ItemDataRole.UserRole)

        from PyQt6.QtWidgets import QMenu
        menu = QMenu()
        entrada = menu.addAction("Entrada de estoque")
        saida = menu.addAction("Saída de estoque")

        action = menu.exec(self.cursor().pos())

        if action == entrada:
            quantidade, ok = QInputDialog.getInt(
                self, "Entrada de estoque", f"Quantidade para adicionar em {nome_item}:"
            )
            registrar_movimentacao(item_id, "ENTRADA", quantidade, self.usuario_id)

            if ok:
                atual = int(self.table.item(row, 4).text())
                nova = atual + quantidade
                atualizar_quantidade(item_id, nova)
                # <-- CORREÇÃO: ENTRADA maiúsculo para respeitar regra do banco
                registrar_movimentacao(item_id, "ENTRADA", quantidade) 
                self.recarregar_tabela()

        elif action == saida:
            
            quantidade, ok = QInputDialog.getInt(
                self, "Saída de estoque", f"Quantidade para retirar de {nome_item}:", 1, 1
            )
            registrar_movimentacao(item_id, "SAIDA", quantidade, self.usuario_id, observacao=destino)
            if not ok: return

            destino, ok = QInputDialog.getText(
                self, "Saída de estoque", f"Para onde vai esta saída?\n(ex: Obra X, Manutenção, Cliente Y)"
            )
            if not ok or not destino.strip():
                QMessageBox.warning(self, "Atenção", "É obrigatório informar o destino.")
                return

            atual = int(self.table.item(row, 4).text())
            if quantidade > atual:
                QMessageBox.warning(self, "Erro", f"Estoque insuficiente! Disponível: {atual}")
                return

            nova = atual - quantidade
            atualizar_quantidade(item_id, nova)
            # <-- CORREÇÃO: SAIDA maiúsculo para respeitar regra do banco
            registrar_movimentacao(item_id, "SAIDA", quantidade, observacao=destino)  
            self.recarregar_tabela()

    def abrir_relatorios(self):
        self.reports_win = ReportsWindow()
        self.reports_win.show()