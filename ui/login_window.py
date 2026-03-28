from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from services.usuario_service import autenticar_usuario

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Estoque TI")
        # Janela maior para um visual mais imponente
        self.setFixedSize(450, 550) 
        # Fundo Azul Escuro fora da borda
        self.setStyleSheet("background-color: #1E293B;") 

        # Layout Principal
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.setContentsMargins(40, 40, 40, 40)

        # --- CARD DE LOGIN ---
        self.card = QFrame()
        # Fundo Bege Claro dentro do card
        self.card.setStyleSheet("""
            QFrame {
                background-color: #e8e0cc;
                border-radius: 20px;
                border: 2px solid #d1c9b8;
            }
            QLabel { 
                border: none; 
                color: #1F2937; 
                font-weight: bold;
                background: transparent;
            }
        """)
        layout_card = QVBoxLayout(self.card)
        layout_card.setSpacing(20)
        layout_card.setContentsMargins(35, 45, 35, 45)

        # Título
        titulo = QLabel("ACESSO AO SISTEMA")
        titulo.setStyleSheet("font-size: 22px; margin-bottom: 10px; color: #1F2937; background: transparent;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_card.addWidget(titulo)

        # Campo Usuário
        layout_card.addWidget(QLabel("Usuário:"))
        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText("Digite seu login...")
        self.input_login.setStyleSheet(self.estilo_input())
        layout_card.addWidget(self.input_login)

        # Campo Senha
        layout_card.addWidget(QLabel("Senha:"))
        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Digite sua senha...")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_senha.setStyleSheet(self.estilo_input())
        layout_card.addWidget(self.input_senha)

        # Botão de Entrar (Ajustado para não cortar e com destaque)
        self.btn_entrar = QPushButton("ENTRAR")
        self.btn_entrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_entrar.setMinimumHeight(55) # Altura maior para o texto não cortar
        self.btn_entrar.setStyleSheet("""
            QPushButton {
                background-color: #1F2937; /* Azul quase preto para contrastar no bege */
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 15px;
                margin-top: 15px;
                border: none;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton:pressed {
                background-color: #0F172A;
            }
        """)
        self.btn_entrar.clicked.connect(self.fazer_login)
        layout_card.addWidget(self.btn_entrar)

        # Botão Criar Conta
        self.btn_registrar = QPushButton("Não tem conta? Registre-se aqui")
        self.btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_registrar.setStyleSheet("""
            QPushButton {
                color: #1F2937;
                text-decoration: underline;
                border: none;
                background: transparent;
                font-size: 12px;
                margin-top: 5px;
            }
            QPushButton:hover {
                color: #475569;
            }
        """)
        self.btn_registrar.clicked.connect(self.abrir_registro)
        layout_card.addWidget(self.btn_registrar)

        layout_principal.addWidget(self.card)
        self.setLayout(layout_principal)

    def estilo_input(self):
        return """
            QLineEdit {
                padding: 12px;
                border: 1px solid #d1c9b8;
                border-radius: 8px;
                background: white;
                color: #333;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #1F2937;
            }
        """

    def fazer_login(self):
        login = self.input_login.text().strip()
        senha = self.input_senha.text().strip()

        if not login or not senha:
            QMessageBox.warning(self, "Aviso", "Por favor, preencha todos os campos.")
            return

        usuario = autenticar_usuario(login, senha)

        if usuario:
            from ui.app_window import AppWindow 
            self.app_window = AppWindow(usuario_id=usuario['id_usuario'], login_window=self)
            self.app_window.show()
            self.hide() 
        else:
            QMessageBox.critical(self, "Erro", "Usuário ou senha incorretos!")

    def abrir_registro(self):
        from ui.register_window import RegisterWindow 
        self.janela_registro = RegisterWindow()
        self.janela_registro.show()