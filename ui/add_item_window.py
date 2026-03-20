from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog,
    QSpinBox, QMessageBox
)

import os
import shutil
import uuid
from services.item_service import adicionar_item


class AddItemWidget(QWidget):
    def __init__(self, atualizar_tabela, voltar_callback):
        super().__init__()
        self.atualizar_tabela = atualizar_tabela
        self.voltar_callback = voltar_callback 
        self.foto_path = ""

        layout = QVBoxLayout()

        # Nome
        layout.addWidget(QLabel("Nome"))
        self.nome = QLineEdit()
        layout.addWidget(self.nome)

        # Caixa
        layout.addWidget(QLabel("Caixa"))
        self.caixa = QLineEdit()
        layout.addWidget(self.caixa)

        # Localização
        layout.addWidget(QLabel("Localização"))
        self.localizacao = QLineEdit()
        layout.addWidget(self.localizacao)

        # Quantidade
        layout.addWidget(QLabel("Quantidade"))
        self.quantidade = QSpinBox()
        self.quantidade.setMaximum(100000)
        layout.addWidget(self.quantidade)

        # Quantidade mínima
        layout.addWidget(QLabel("Quantidade mínima"))
        self.quantidade_minima = QSpinBox()
        self.quantidade_minima.setMaximum(100000)
        layout.addWidget(self.quantidade_minima)

        # Botão selecionar foto
        self.btn_foto = QPushButton("Selecionar Foto")
        self.btn_foto.clicked.connect(self.selecionar_foto)
        layout.addWidget(self.btn_foto)

        # Botão salvar
        self.btn_salvar = QPushButton("Salvar Item")
        self.btn_salvar.clicked.connect(self.salvar_item)
        layout.addWidget(self.btn_salvar)

        self.setLayout(layout)

    def selecionar_foto(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Foto",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file:
            self.foto_path = file
            self.btn_foto.setText("Foto Selecionada!") 

    def salvar_item(self):

        nome = self.nome.text()
        caixa = self.caixa.text()
        localizacao = self.localizacao.text()
        quantidade = self.quantidade.value()
        quantidade_minima = self.quantidade_minima.value()
        
        if not nome:
            QMessageBox.warning(self, "Erro", "Digite o nome do item")
            return

        # --- NOVA LÓGICA DE TRATAMENTO DA IMAGEM ---
        caminho_banco = ""

        if self.foto_path:
            # Cria uma pasta 'fotos' na raiz do projeto se ela não existir
            os.makedirs("fotos", exist_ok=True)
            
            # Pega a extensão original do arquivo (ex: .png, .jpg)
            extensao = os.path.splitext(self.foto_path)[1]
            
            # Cria um nome único aleatório para não dar conflito
            novo_nome = f"{uuid.uuid4().hex}{extensao}"
            
            # Define o destino final da imagem
            caminho_dest = os.path.join("fotos", novo_nome)
            
            try:
                # Copia a imagem do PC do usuário para a pasta do projeto
                shutil.copy(self.foto_path, caminho_dest)
                caminho_banco = caminho_dest
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível processar a imagem: {e}")
                return
        # ---------------------------------------------

        adicionar_item(
            nome,
            caixa,
            localizacao,
            quantidade,
            quantidade_minima,
            caminho_banco 
        )

        QMessageBox.information(self, "", "Item adicionado!")
        self.atualizar_tabela()
        self.voltar_callback()