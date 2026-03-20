from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from services.usuario_service import registrar_usuario

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Criar Nova Conta")
        self.resize(300, 350)

        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Cadastro de Usuário")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        # Nome
        layout.addWidget(QLabel("Nome Completo:"))
        self.input_nome = QLineEdit()
        layout.addWidget(self.input_nome)

        # Login
        layout.addWidget(QLabel("Nome de Usuário:"))
        self.input_login = QLineEdit()
        layout.addWidget(self.input_login)

        # Senha
        layout.addWidget(QLabel("Senha:"))
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_senha)

        # Confirmar Senha
        layout.addWidget(QLabel("Confirme a Senha:"))
        self.input_confirma_senha = QLineEdit()
        self.input_confirma_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_confirma_senha)

        # Botão Cadastrar
        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.setStyleSheet("margin-top: 15px; padding: 5px;")
        self.btn_cadastrar.clicked.connect(self.salvar_cadastro)
        layout.addWidget(self.btn_cadastrar)

        self.setLayout(layout)

    def salvar_cadastro(self):
        nome = self.input_nome.text()
        login = self.input_login.text().strip()
        senha = self.input_senha.text()
        confirma = self.input_confirma_senha.text()

        # Validações simples
        if not nome or not login or not senha:
            QMessageBox.warning(self, "Atenção", "Preencha todos os campos!")
            return
            
        if senha != confirma:
            QMessageBox.warning(self, "Atenção", "As senhas não coincidem!")
            return

        # Tenta salvar no banco
        sucesso, mensagem = registrar_usuario(nome, login, senha)

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.close() # Fecha a janela após cadastrar
        else:
            QMessageBox.critical(self, "Erro", mensagem)