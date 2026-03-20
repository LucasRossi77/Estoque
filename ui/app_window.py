from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QStackedWidget, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from ui.profile_window import PerfilWidget
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
from ui.main_window import EstoqueWidget
from ui.reports_window import ReportsWindow
from ui.add_item_window import AddItemWidget
from ui.edit_item_window import EditItemWidget

class AppWindow(QMainWindow):
    def __init__(self, usuario_id, login_window): 
        super().__init__()
        self.usuario_id = usuario_id
        self.login_window = login_window 

        self.setWindowTitle("Sistema de Gestão - TI")
        self.resize(1100, 700)

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget) 
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # MENU LATERAL 
        menu_widget = QWidget()
        menu_widget.setFixedWidth(220)
        menu_widget.setStyleSheet("background-color: #2c3e50; color: white;")
        self.menu_layout = QVBoxLayout(menu_widget)

        # Botões do Menu 
        self.btn_perfil = self.criar_botao_menu("👤   Perfil")
        self.btn_estoque = self.criar_botao_menu("📦   Estoque")
        self.btn_relatorios = self.criar_botao_menu("📊   Relatórios")
        
        self.btn_sair = self.criar_botao_menu("🚪   Sair")
        self.btn_sair.setStyleSheet(self.btn_sair.styleSheet() + "color: #ff4d4d;")
        self.btn_sair.clicked.connect(self.logout)

        
        self.menu_layout.addWidget(self.btn_perfil)
        self.menu_layout.addWidget(self.btn_estoque)
        self.menu_layout.addWidget(self.btn_relatorios)
        
        self.menu_layout.addStretch() # Empurra o Sair para baixo
        self.menu_layout.addWidget(self.btn_sair)

        
        self.stacked_widget = QStackedWidget() 

        self.tela_perfil = PerfilWidget()
        self.tela_estoque = EstoqueWidget(
            self.usuario_id, 
            self.ir_para_adicionar, 
            self.ir_para_editar     
        )
        self.tela_relatorios = ReportsWindow()
        
        
        self.tela_adicionar = AddItemWidget(self.tela_estoque.carregar_itens, self.voltar_para_estoque)

       
        self.stacked_widget.addWidget(self.tela_perfil)      # Índice 0
        self.stacked_widget.addWidget(self.tela_estoque)     # Índice 1
        self.stacked_widget.addWidget(self.tela_relatorios)  # Índice 2
        self.stacked_widget.addWidget(self.tela_adicionar)   # Índice 3

       
        main_layout.addWidget(menu_widget)     # Lado esquerdo
        main_layout.addWidget(self.stacked_widget) # Lado direito

        # Conectar Cliques do Menu
        self.btn_perfil.clicked.connect(lambda: self.mudar_tela(0))
        self.btn_estoque.clicked.connect(lambda: self.mudar_tela(1))
        self.btn_relatorios.clicked.connect(lambda: self.mudar_tela(2))

    def criar_botao_menu(self, texto):
        btn = QPushButton(texto)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 15px;
                font-size: 15px;
                border: none;
            }
            QPushButton:hover { background-color: #34495e; }
        """)
        return btn

    def mudar_tela(self, index):
        self.stacked_widget.setCurrentIndex(index)
        if index == 2:
            self.tela_relatorios.carregar_dados()

    
    def ir_para_adicionar(self):
        self.stacked_widget.setCurrentIndex(3) # Cadastro é o 3

    def ir_para_editar(self, item_id):
        self.tela_editar = EditItemWidget(item_id, self.tela_estoque.carregar_itens, self.voltar_para_estoque)
        
        # Remove edição anterior se existir para não acumular memória
        if self.stacked_widget.count() > 4:
            self.stacked_widget.removeWidget(self.stacked_widget.widget(4))
            
        self.stacked_widget.addWidget(self.tela_editar)
        self.stacked_widget.setCurrentIndex(4) # Edição será o 4

    def voltar_para_estoque(self):
        self.stacked_widget.setCurrentIndex(1) # Estoque agora é o índice 1

    def logout(self):
        self.close()
        self.login_window.show()    