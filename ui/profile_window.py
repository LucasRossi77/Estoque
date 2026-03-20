from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class PerfilWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título
        titulo = QLabel("👤 Perfil")
        titulo.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # Área de Informações (Simulada)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        self.label_nome = QLabel("<b>Nome:</b> Usuário Administrador")
        self.label_cargo = QLabel("<b>Cargo:</b> Gestor de TI")
        self.label_setor = QLabel("<b>Setor:</b> Infraestrutura")
        
        for lb in [self.label_nome, self.label_cargo, self.label_setor]:
            lb.setStyleSheet("font-size: 16px;")
            info_layout.addWidget(lb)

        layout.addLayout(info_layout)
        self.setLayout(layout)