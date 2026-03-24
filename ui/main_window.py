from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
    QAbstractItemView, QInputDialog, QMessageBox
)
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtCore import Qt 

from services.item_service import listar_itens, atualizar_quantidade
from utils.alertas import estoque_baixo
from services.movimentacao_service import registrar_movimentacao

class EstoqueWidget(QWidget):
    def __init__(self, usuario_id, callback_add, callback_edit):
        super().__init__()
        self.usuario_id = usuario_id
        self.callback_add = callback_add   
        self.callback_edit = callback_edit 
        self.setStyleSheet("background-color: #e8e0cc;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # 1. Primeiro criamos a barra e os componentes
        barra = QHBoxLayout()
        self.search = QLineEdit()
        self.search.textChanged.connect(self.filtrar_itens)
        self.search.setPlaceholderText("Pesquisar item...")
        
        btn_add = QPushButton("Adicionar Item")
        
        # 2. DEPOIS de criar o btn_add, nós fazemos o connect
        btn_add.clicked.connect(self.callback_add) 

        barra.addWidget(self.search)
        barra.addWidget(btn_add)
        layout.addLayout(barra)

        # TABELA
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Foto", "Nome", "Caixa", "Localização", "Quantidade", "Min"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
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
                        cell.setBackground(QColor(255,90,90))

    def filtrar_itens(self):
        texto = self.search.text().lower()
        
        for row in range(self.table.rowCount()):
            # Pegamos o texto das 3 colunas
            nome = self.table.item(row, 1).text().lower() if self.table.item(row, 1) else ""
            caixa = self.table.item(row, 2).text().lower() if self.table.item(row, 2) else ""
            local = self.table.item(row, 3).text().lower() if self.table.item(row, 3) else ""
            
            # Se o texto pesquisado estiver no Nome, OU na Caixa, OU no Local -> Mostra a linha
            if texto in nome or texto in caixa or texto in local:
                self.table.setRowHidden(row, False)
            else:
                # Se não achar em nenhum dos três -> Esconde a linha
                self.table.setRowHidden(row, True)

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
        menu.addSeparator() # Linha divisória para organizar
        editar = menu.addAction("Editar Item")
        excluir = menu.addAction("Excluir Item")

        action = menu.exec(self.cursor().pos())

        if action == entrada:
            
            quantidade, ok = QInputDialog.getInt(self, "Entrada de estoque", f"Quantidade para adicionar em {nome_item}:")
            if ok:
                atual = int(self.table.item(row, 4).text())
                nova = atual + quantidade
                atualizar_quantidade(item_id, nova)
                registrar_movimentacao(item_id, "ENTRADA", quantidade, self.usuario_id) 
                self.recarregar_tabela()

        elif action == saida:
            
            quantidade, ok = QInputDialog.getInt(self, "Saída de estoque", f"Quantidade para retirar de {nome_item}:", 1, 1)
            if not ok: return
            observacao, ok = QInputDialog.getText(self, "Saída de estoque", f"Observação")
            if not ok or not observacao.strip():
                QMessageBox.warning(self, "Atenção", "É obrigatório informar Observação.")
                return
            atual = int(self.table.item(row, 4).text())
            if quantidade > atual:
                QMessageBox.warning(self, "Erro", f"Estoque insuficiente! Disponível: {atual}")
                return
            nova = atual - quantidade
            atualizar_quantidade(item_id, nova)
            registrar_movimentacao(item_id, "SAIDA", quantidade, self.usuario_id, observacao=observacao)  
            self.recarregar_tabela()

    
        elif action == editar:
            self.callback_edit(item_id)

        elif action == excluir:
            
            resposta = QMessageBox.question(
                self, "Confirmar Exclusão",
                f"Tem certeza que deseja excluir o item '{nome_item}'?\nIsso não pode ser desfeito.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if resposta == QMessageBox.StandardButton.Yes:
                from services.item_service import excluir_item
                excluir_item(item_id)
                self.recarregar_tabela()
