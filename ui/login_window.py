from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from services.usuario_service import autenticar_usuario
from ui.app_window import AppWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Estoque TI")
        self.resize(300, 250)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        titulo = QLabel("Acesso ao Estoque")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(titulo)

        # Campo Usuário
        layout.addWidget(QLabel("Nome de Usuário:"))
        self.input_login = QLineEdit()
        layout.addWidget(self.input_login)

        # Campo Senha
        layout.addWidget(QLabel("Senha:"))
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_senha)

        # Botão de Entrar
        self.btn_entrar = QPushButton("Entrar")
        self.btn_entrar.setStyleSheet("margin-top: 10px; padding: 5px;")
        self.btn_entrar.clicked.connect(self.fazer_login)
        layout.addWidget(self.btn_entrar)

        # Botão Criar Conta
        self.btn_registrar = QPushButton("Criar Conta!")
        self.btn_registrar.setStyleSheet("color: blue; text-decoration: underline; border: none; background: transparent; margin-top: 5px;")
        self.btn_registrar.clicked.connect(self.abrir_registro)
        layout.addWidget(self.btn_registrar)

        self.setLayout(layout)

    def fazer_login(self):
        
        login = self.input_login.text()
        senha = self.input_senha.text()

        
        if not login or not senha:
            QMessageBox.warning(self, "", "Preencha todos os campos!")
            return

        usuario = autenticar_usuario(login, senha)

        if usuario:
            
            from ui.app_window import AppWindow 
            self.app_window = AppWindow(usuario_id=usuario['id_usuario'], login_window=self)
            self.app_window.show()
            self.hide() 
        else:
            QMessageBox.critical(self, "", "Dados incorretos!")

    def abrir_registro(self):
        from ui.register_window import RegisterWindow 
        self.janela_registro = RegisterWindow()
        self.janela_registro.show()