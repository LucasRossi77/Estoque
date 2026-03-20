from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QMessageBox
)
from services.item_service import buscar_item_por_id, atualizar_item

class EditItemWidget(QWidget): # <--- Aqui estava "Windet", mude para "Widget"
    def __init__(self, item_id, atualizar_tabela, voltar_callback):
        super().__init__()
        self.item_id = item_id # <--- ADICIONE ESTA LINHA (faltou no seu código)
        self.atualizar_tabela = atualizar_tabela
        self.voltar_callback = voltar_callback

        self.setWindowTitle("Editar Item")
        self.setGeometry(250, 250, 300, 350)

        layout = QVBoxLayout()

        # Pegar dados atuais do banco
        item_atual = buscar_item_por_id(self.item_id)

        # Nome
        layout.addWidget(QLabel("Nome"))
        self.nome = QLineEdit(item_atual["nome"])
        layout.addWidget(self.nome)

        # Caixa
        layout.addWidget(QLabel("Caixa"))
        self.caixa = QLineEdit(str(item_atual["caixa"]))
        layout.addWidget(self.caixa)

        # Localização
        layout.addWidget(QLabel("Localização"))
        self.localizacao = QLineEdit(str(item_atual["localizacao"]))
        layout.addWidget(self.localizacao)

        # Quantidade mínima
        layout.addWidget(QLabel("Quantidade Mínima de Alerta"))
        self.quantidade_minima = QSpinBox()
        self.quantidade_minima.setMaximum(100000)
        self.quantidade_minima.setValue(item_atual["quantidade_minima"])
        layout.addWidget(self.quantidade_minima)

        # Botão salvar
        self.btn_salvar = QPushButton("Salvar Alterações")
        self.btn_salvar.clicked.connect(self.salvar_edicao)
        layout.addWidget(self.btn_salvar)

        self.setLayout(layout)

    def salvar_edicao(self):
        nome = self.nome.text()
        caixa = self.caixa.text()
        localizacao = self.localizacao.text()
        qtd_min = self.quantidade_minima.value()

        if not nome:
            QMessageBox.warning(self, "Erro", "O nome não pode ficar vazio.")
            return

        atualizar_item(self.item_id, nome, caixa, localizacao, qtd_min)
        QMessageBox.information(self, "Sucesso", "Item atualizado com sucesso!")
        
        self.atualizar_tabela()
        self.voltar_callback() 