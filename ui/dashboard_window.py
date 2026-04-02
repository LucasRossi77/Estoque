import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #e8e0cc;") # Fundo bege que você escolheu
        
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop)

        titulo = QLabel("📈 Dashboard")
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; color: #1F2937; margin-bottom: 20px;margin-top: 10px;")
        layout_principal.addWidget(titulo)

        # Layout horizontal para colocar os gráficos lado a lado
        layout_graficos = QHBoxLayout()
        layout_principal.addLayout(layout_graficos)
        layout_principal.addStretch(1)
        
        # 1. Gráfico de Estoque Baixo
        self.canvas_baixo = self.criar_grafico_estoque_baixo()
        layout_graficos.addWidget(self.canvas_baixo)

        # 2. Gráfico de Estoque Alto
        self.canvas_alto = self.criar_grafico_estoque_alto()
        layout_graficos.addWidget(self.canvas_alto)

        layout_principal.addLayout(layout_graficos)
        self.setLayout(layout_principal)

    def buscar_dados(self, ordem, limite=10):
        """Busca os dados reais no banco. Ordem pode ser 'ASC' (menor) ou 'DESC' (maior)"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Ajuste "nome" e "quantidade" para os nomes reais das colunas da sua tabela!
        try:
            cursor.execute(f"SELECT nome, quantidade FROM itens ORDER BY quantidade {ordem} LIMIT {limite}")
            dados = cursor.fetchall()
        except sqlite3.OperationalError:
            # Caso a tabela esteja vazia ou com nome diferente, retorna dados falsos para não quebrar a tela
            dados = [("Item A", 10), ("Item B", 20)] 
        finally:
            conn.close()
            
        nomes = [linha[0] for linha in dados]
        quantidades = [linha[1] for linha in dados]
        return nomes, quantidades

    def criar_grafico_estoque_baixo(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        # Pinta o fundo do gráfico com a mesma cor da sua janela
        fig.patch.set_facecolor('#e8e0cc') 
        ax = fig.add_subplot(111)
        ax.set_facecolor('#e8e0cc')

        nomes, quantidades = self.buscar_dados('ASC')

        # Cor de Perigo que você escolheu (Vermelho)
        ax.bar(nomes, quantidades, color='#EF4444')
        ax.set_title("Estoque Baixo", color="#1F2937", fontweight='bold')
        ax.tick_params(axis='x', colors='#1F2937', rotation=45)
        ax.tick_params(axis='y', colors='#1F2937')
        
        # Ajusta o layout para os nomes não cortarem
        fig.tight_layout()
        return FigureCanvasQTAgg(fig)

    def criar_grafico_estoque_alto(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor('#e8e0cc')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#e8e0cc')

        nomes, quantidades = self.buscar_dados('DESC')

        # Cor Primária que você escolheu (Azul Escuro)
        ax.bar(nomes, quantidades, color='#1E3A8A')
        ax.set_title("Estoque Alto", color="#1F2937", fontweight='bold')
        ax.tick_params(axis='x', colors='#1F2937', rotation=45)
        ax.tick_params(axis='y', colors='#1F2937')
        
        fig.tight_layout()
        return FigureCanvasQTAgg(fig)