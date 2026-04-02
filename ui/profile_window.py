from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QHBoxLayout, QInputDialog
)
from PyQt6.QtCore import Qt
# IMPORTANTE: Adicionamos o autenticar_usuario aqui na lista de importações!
from services.usuario_service import (
    obter_usuario_por_id, atualizar_dados_usuario, 
    atualizar_senha_usuario, excluir_usuario_db, autenticar_usuario
)

class PerfilWidget(QWidget):
    def __init__(self, usuario_id, callback_logout):
        super().__init__()
        self.usuario_id = usuario_id
        self.callback_logout = callback_logout
        self.login_atual = "" # Vamos guardar o login para facilitar a verificação da senha
        self.setStyleSheet("background-color: #e8e0cc;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        titulo = QLabel("👤 Meu Perfil")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # --- CAMPOS DE INFORMAÇÃO ---
        layout.addWidget(QLabel("Nome Completo:"))
        self.input_nome = QLineEdit()
        layout.addWidget(self.input_nome)

        layout.addWidget(QLabel("Nome de Usuário (Login):"))
        self.input_login = QLineEdit()
        layout.addWidget(self.input_login)

        # --- BOTÕES DE EDIÇÃO (Lado a Lado) ---
        botoes_edicao_layout = QHBoxLayout()
        
        self.btn_editar = QPushButton("✏️ Editar Informações")
        self.btn_editar.setStyleSheet("background-color: #E0B041; color: white; padding: 8px;")
        self.btn_editar.clicked.connect(self.habilitar_edicao)
        
        self.btn_salvar = QPushButton("💾 Salvar Alterações")
        self.btn_salvar.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")
        self.btn_salvar.clicked.connect(self.salvar_dados)
        
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_cancelar.setStyleSheet("background-color: #7f8c8d; color: white; padding: 8px;")
        self.btn_cancelar.clicked.connect(self.cancelar_edicao)

        botoes_edicao_layout.addWidget(self.btn_editar)
        botoes_edicao_layout.addWidget(self.btn_salvar)
        botoes_edicao_layout.addWidget(self.btn_cancelar)
        layout.addLayout(botoes_edicao_layout)

        layout.addSpacing(30) # Dá um respiro na tela

        # --- ÁREA DE SEGURANÇA ---
        titulo_seguranca = QLabel("🔒 Segurança e Conta")
        titulo_seguranca.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo_seguranca)

        botoes_seguranca_layout = QHBoxLayout()
        
        self.btn_senha = QPushButton("🔑 Mudar Senha")
        self.btn_senha.setStyleSheet("background-color: #E0B041; color: white; padding: 8px;")
        self.btn_senha.clicked.connect(self.mudar_senha)
        
        btn_excluir = QPushButton("🗑️ Excluir Conta")
        btn_excluir.setStyleSheet("background-color: #c0392b; color: white; padding: 8px;")
        btn_excluir.clicked.connect(self.excluir_conta)

        botoes_seguranca_layout.addWidget(self.btn_senha)
        botoes_seguranca_layout.addWidget(btn_excluir)
        layout.addLayout(botoes_seguranca_layout)

        self.setLayout(layout)
        
        self.carregar_dados()
        self.travar_campos()

    def carregar_dados(self):
        usuario = obter_usuario_por_id(self.usuario_id)
        if usuario:
            self.input_nome.setText(usuario['nome'])
            self.input_login.setText(usuario['login'])
            self.login_atual = usuario['login'] # Guarda na memória

    def travar_campos(self):
        self.input_nome.setReadOnly(True)
        self.input_login.setReadOnly(True)
        
        estilo_bloqueado = "background-color: #f2f2f2; border: 1px solid #ccc; color: #555; padding: 5px;"
        self.input_nome.setStyleSheet(estilo_bloqueado)
        self.input_login.setStyleSheet(estilo_bloqueado)

        self.btn_editar.setVisible(True)
        self.btn_salvar.setVisible(False)
        self.btn_cancelar.setVisible(False)

    def habilitar_edicao(self):
        """Libera a edição e muda a cor para branco"""
        self.input_nome.setReadOnly(False)
        self.input_login.setReadOnly(False)
        
        estilo_livre = "background-color: white; border: 1px solid #3498db; color: black; padding: 5px;"
        self.input_nome.setStyleSheet(estilo_livre)
        self.input_login.setStyleSheet(estilo_livre)

        self.btn_editar.setVisible(False)
        self.btn_salvar.setVisible(True)
        self.btn_cancelar.setVisible(True)

    def cancelar_edicao(self):
        self.carregar_dados()
        self.travar_campos()

    def salvar_dados(self):
        novo_nome = self.input_nome.text()
        novo_login = self.input_login.text()
        
        if not novo_nome or not novo_login:
            QMessageBox.warning(self, "", "Os campos não podem ficar vazios!")
            return

        atualizar_dados_usuario(self.usuario_id, novo_nome, novo_login)
        self.login_atual = novo_login # Atualiza na memória
        QMessageBox.information(self, "", "Dados atualizados com sucesso!")
        self.travar_campos() # Salva e trava os campos automaticamente

    def mudar_senha(self):
        # Pedir a senha antiga
        senha_antiga, ok = QInputDialog.getText(
            self, "", "Para liberar a troca, digite sua senha atual:", 
            QLineEdit.EchoMode.Password
        )
        
        if not ok or not senha_antiga:
            return # Se cancelar ou der enter vazio, não faz nada
            
        # Validar a senha antiga
        if not autenticar_usuario(self.login_atual, senha_antiga):
            QMessageBox.critical(self, "", "A senha atual está incorreta!")
            return

        # Se estiver correta, pedir a NOVA senha
        nova_senha, ok_nova = QInputDialog.getText(
            self, "", "Digite sua nova senha:", 
            QLineEdit.EchoMode.Password
        )
        
        if ok_nova and nova_senha:
            # 4. PASSO: Pedir para confirmar a nova senha (evita erros de digitação)
            confirmar_senha, ok_conf = QInputDialog.getText(
                self, "", "Digite a nova senha novamente para confirmar:", 
                QLineEdit.EchoMode.Password
            )
            
            if ok_conf and nova_senha == confirmar_senha:
                atualizar_senha_usuario(self.usuario_id, nova_senha)
                QMessageBox.information(self, "", "Sua senha foi alterada com sucesso!")
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
            QMessageBox.warning(self, "", "Sua conta foi excluída.")
            self.callback_logout()