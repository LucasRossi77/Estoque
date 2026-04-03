from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from services.usuario_service import (
    obter_usuario_por_id, atualizar_dados_usuario, 
    atualizar_senha_usuario, excluir_usuario_db, autenticar_usuario
)
from PyQt6.QtWidgets import QInputDialog

class PerfilWidget(QWidget):
    def __init__(self, usuario_id, callback_logout):
        super().__init__()
        self.usuario_id = usuario_id
        self.callback_logout = callback_logout
        self.login_atual = "" 
        
        self.setStyleSheet("background-color: #e8e0cc;")

        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout_principal.setContentsMargins(20, 40, 20, 20)

        # ==========================================
        # CARD PRINCIPAL
        # ==========================================
        self.card = QFrame()
        self.card.setFixedWidth(400)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #d1c9b8;
            }
        """)
        
        layout_card = QVBoxLayout(self.card)
        layout_card.setContentsMargins(30, 30, 30, 30)
        layout_card.setSpacing(10)

        # --- AVATAR (Círculo no topo) ---
        lbl_avatar = QLabel("👤")
        lbl_avatar.setFixedSize(70, 70)
        lbl_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_avatar.setStyleSheet("""
            QLabel {
                background-color: #f1f5f9;
                color: #64748b;
                font-size: 35px;
                border-radius: 35px; /* Deixa redondo */
                border: 2px solid #e2e8f0;
            }
        """)
        
        layout_avatar = QHBoxLayout()
        layout_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_avatar.addWidget(lbl_avatar)
        layout_card.addLayout(layout_avatar)

        # Título
        titulo = QLabel("Meu Perfil")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1F2937; margin-bottom: 20px; border: none;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_card.addWidget(titulo)

        # ==========================================
        # ESTILOS DOS INPUTS (LEITURA VS EDIÇÃO)
        # ==========================================
        self.estilo_readonly = """
            QLineEdit {
                padding: 8px 0px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                background-color: transparent;
                font-size: 16px;
                color: #1F2937;
                font-weight: bold;
            }
        """
        self.estilo_edit = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #3b82f6;
                border-radius: 6px;
                background-color: #f8fafc;
                font-size: 15px;
                color: #1e293b;
            }
        """

        # --- CAMPOS ---
        lbl_nome = QLabel("NOME COMPLETO")
        lbl_nome.setStyleSheet("font-size: 11px; font-weight: bold; color: #94a3b8; border: none;")
        layout_card.addWidget(lbl_nome)
        
        self.input_nome = QLineEdit()
        self.input_nome.setReadOnly(True)
        self.input_nome.setStyleSheet(self.estilo_readonly)
        layout_card.addWidget(self.input_nome)

        layout_card.addSpacing(10)

        lbl_login = QLabel("USUÁRIO (LOGIN)")
        lbl_login.setStyleSheet("font-size: 11px; font-weight: bold; color: #94a3b8; border: none;")
        layout_card.addWidget(lbl_login)
        
        self.input_login = QLineEdit()
        self.input_login.setReadOnly(True)
        self.input_login.setStyleSheet(self.estilo_readonly)
        layout_card.addWidget(self.input_login)

        layout_card.addSpacing(20)

        # ==========================================
        # BOTÕES DE CONTROLE DE EDIÇÃO
        # ==========================================
        self.layout_botoes_edicao = QHBoxLayout()
        
        self.btn_editar = QPushButton("✏️ Editar Dados")
        self.btn_editar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_editar.setStyleSheet("""
            QPushButton { background-color: #f1f5f9; color: #334155; font-weight: bold; border-radius: 6px; padding: 10px; border: none; }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        self.btn_editar.clicked.connect(lambda: self.alternar_modo_edicao(True))

        self.btn_cancelar = QPushButton("✖ Cancelar")
        self.btn_cancelar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancelar.setStyleSheet("""
            QPushButton { background-color: #fef2f2; color: #ef4444; font-weight: bold; border-radius: 6px; padding: 10px; border: none; }
            QPushButton:hover { background-color: #fee2e2; }
        """)
        self.btn_cancelar.clicked.connect(self.cancelar_edicao)
        self.btn_cancelar.hide()

        self.btn_salvar = QPushButton("💾 Salvar")
        self.btn_salvar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_salvar.setStyleSheet("""
            QPushButton { background-color: #10B981; color: white; font-weight: bold; border-radius: 6px; padding: 10px; border: none; }
            QPushButton:hover { background-color: #059669; }
        """)
        self.btn_salvar.clicked.connect(self.salvar_perfil)
        self.btn_salvar.hide()

        self.layout_botoes_edicao.addWidget(self.btn_editar)
        self.layout_botoes_edicao.addWidget(self.btn_cancelar)
        self.layout_botoes_edicao.addWidget(self.btn_salvar)
        
        layout_card.addLayout(self.layout_botoes_edicao)

        # --- LINHA DIVISÓRIA ---
        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        linha.setStyleSheet("border-top: 1px solid #e2e8f0; margin: 15px 0; border-left: none; border-right: none; border-bottom: none;")
        layout_card.addWidget(linha)

        # ==========================================
        # BOTÕES DE SEGURANÇA
        # ==========================================
        self.btn_alterar_senha = QPushButton("🔑 Alterar Senha")
        self.btn_alterar_senha.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_alterar_senha.setStyleSheet("""
            QPushButton { background-color: #3B82F6; color: white; font-weight: bold; border-radius: 6px; padding: 10px; border: none; }
            QPushButton:hover { background-color: #2563EB; }
        """)
        self.btn_alterar_senha.clicked.connect(self.alterar_senha)
        layout_card.addWidget(self.btn_alterar_senha)

        self.btn_excluir = QPushButton("Excluir Minha Conta")
        self.btn_excluir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_excluir.setStyleSheet("""
            QPushButton { background-color: transparent; color: #94a3b8; text-decoration: underline; font-weight: bold; padding: 5px; border: none; margin-top: 10px; }
            QPushButton:hover { color: #EF4444; }
        """)
        self.btn_excluir.clicked.connect(self.excluir_conta)
        layout_card.addWidget(self.btn_excluir)

        layout_principal.addWidget(self.card)
        layout_principal.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.carregar_dados()

    # ==========================================
    # LÓGICA DE INTERFACE E DADOS
    # ==========================================
    def carregar_dados(self):
        usuario = obter_usuario_por_id(self.usuario_id)
        if usuario:
            self.input_nome.setText(usuario['nome'])
            self.input_login.setText(usuario['login'])
            self.login_atual = usuario['login']

    def alternar_modo_edicao(self, ativado):
        self.input_nome.setReadOnly(not ativado)
        self.input_login.setReadOnly(not ativado)
        
        if ativado:
            self.input_nome.setStyleSheet(self.estilo_edit)
            self.input_login.setStyleSheet(self.estilo_edit)
            self.btn_editar.hide()
            self.btn_cancelar.show()
            self.btn_salvar.show()
            self.input_nome.setFocus()
        else:
            self.input_nome.setStyleSheet(self.estilo_readonly)
            self.input_login.setStyleSheet(self.estilo_readonly)
            self.btn_cancelar.hide()
            self.btn_salvar.hide()
            self.btn_editar.show()

    def cancelar_edicao(self):
        # Recarrega os dados do banco para desfazer o que o usuário digitou
        self.carregar_dados() 
        self.alternar_modo_edicao(False)

    def salvar_perfil(self):
        novo_nome = self.input_nome.text().strip()
        novo_login = self.input_login.text().strip()

        if not novo_nome or not novo_login:
            QMessageBox.warning(self, "Aviso", "Os campos não podem ficar vazios!")
            return

        sucesso, mensagem = atualizar_dados_usuario(self.usuario_id, novo_nome, novo_login)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.login_atual = novo_login
            self.alternar_modo_edicao(False) # Volta pro modo leitura!
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def alterar_senha(self):
        senha_antiga, ok = QInputDialog.getText(
            self, "Segurança", "Para continuar, digite sua senha ATUAL:", 
            QLineEdit.EchoMode.Password
        )
        
        if not ok or not senha_antiga:
            return 
            
        if not autenticar_usuario(self.login_atual, senha_antiga):
            QMessageBox.critical(self, "Erro", "A senha atual está incorreta!")
            return

        nova_senha, ok_nova = QInputDialog.getText(
            self, "Nova Senha", "Digite sua nova senha:", 
            QLineEdit.EchoMode.Password
        )
        
        if ok_nova and nova_senha:
            confirmar_senha, ok_conf = QInputDialog.getText(
                self, "Confirmação", "Digite a nova senha novamente para confirmar:", 
                QLineEdit.EchoMode.Password
            )
            
            if ok_conf and nova_senha == confirmar_senha:
                atualizar_senha_usuario(self.usuario_id, nova_senha)
                QMessageBox.information(self, "Sucesso", "Sua senha foi alterada com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "As senhas não coincidem. Tente novamente.")

    def excluir_conta(self):
        resposta = QMessageBox.question(
            self, "Excluir Conta", 
            "Tem certeza que deseja excluir sua conta?\nTodos os seus acessos serão perdidos.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if resposta == QMessageBox.StandardButton.Yes:
            excluir_usuario_db(self.usuario_id)
            QMessageBox.warning(self, "Conta Excluída", "Sua conta foi excluída.")
            self.callback_logout()