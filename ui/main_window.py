import sqlite3
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QAbstractItemView, QSpinBox 
)
from datetime import datetime 
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QIcon, QPixmap

class EstoqueWidget(QWidget):
    def __init__(self, usuario_id, callback_adicionar, callback_editar):
        super().__init__()
        self.usuario_id = usuario_id
        self.callback_adicionar = callback_adicionar
        self.callback_editar = callback_editar
        
        # Caminhos
        pasta_ui = os.path.dirname(os.path.abspath(__file__))
        self.caminho_db = os.path.abspath(os.path.join(pasta_ui, "..", "database.db"))
        self.pasta_fotos = os.path.abspath(os.path.join(pasta_ui, "..")) 
        
        self.setStyleSheet("background-color: #e8e0cc;")
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # 1. CABEÇALHO
        lbl_titulo = QLabel("Controle de Estoque")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1F2937;")
        layout_principal.addWidget(lbl_titulo)

        # 2. CARTÕES DE MÉTRICAS (Resumo)
        layout_cards = QHBoxLayout()
        self.lbl_total_itens = self.criar_cartao(layout_cards, "Itens Cadastrados")
        self.lbl_unidades = self.criar_cartao(layout_cards, "Unidades em Estoque")
        self.lbl_estoque_baixo = self.criar_cartao(layout_cards, "Estoque Baixo")
        self.lbl_movimentacoes = self.criar_cartao(layout_cards, "Movimentações Hoje")
        layout_principal.addLayout(layout_cards)

        # 3. BARRA DE FILTROS E BUSCA
        frame_filtros = QFrame()
        frame_filtros.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #d1c9b8;")
        layout_f = QHBoxLayout(frame_filtros)
        
        self.txt_filtro_nome = QLineEdit(); self.txt_filtro_nome.setPlaceholderText("🔍 Buscar por nome...")
        self.txt_filtro_local = QLineEdit(); self.txt_filtro_local.setPlaceholderText("📍 Localização...")
        self.txt_filtro_caixa = QLineEdit(); self.txt_filtro_caixa.setPlaceholderText("📦 Caixa...")
        
        # Estilo dos inputs
        estilo_input = "padding: 8px; border: 1px solid #ccc; border-radius: 4px; background: #f9f9f9;"
        self.txt_filtro_nome.setStyleSheet(estilo_input)
        self.txt_filtro_local.setStyleSheet(estilo_input)
        self.txt_filtro_caixa.setStyleSheet(estilo_input)
        
        btn_limpar = QPushButton("Limpar Filtros")
        btn_limpar.clicked.connect(self.limpar_filtros)
        
        # Conecta o evento de digitar à busca automática
        self.txt_filtro_nome.textChanged.connect(self.carregar_itens)
        self.txt_filtro_local.textChanged.connect(self.carregar_itens)
        self.txt_filtro_caixa.textChanged.connect(self.carregar_itens)

        layout_f.addWidget(QLabel("Filtros:"))
        layout_f.addWidget(self.txt_filtro_nome)
        layout_f.addWidget(self.txt_filtro_local)
        layout_f.addWidget(self.txt_filtro_caixa)
        layout_f.addWidget(btn_limpar)
        layout_principal.addWidget(frame_filtros)

        # 4. BOTÕES DE AÇÃO E MOVIMENTAÇÃO RÁPIDA
        layout_acoes = QHBoxLayout()
        
        # Grupo 1: Botões CRUD
        layout_crud = QHBoxLayout()
        layout_crud.addWidget(self.criar_botao_acao("Adicionar", "#9c9075", self.callback_adicionar))
        layout_crud.addWidget(self.criar_botao_acao("Editar", "#9c9075", self.editar_selecionado))
        layout_crud.addWidget(self.criar_botao_acao("Excluir", "#9c9075", self.deletar_item))
        layout_acoes.addLayout(layout_crud)
        
        layout_acoes.addStretch() # Espaço flexível para empurrar as movimentações para a direita
        
        # Grupo 2: Painel Integrado de Movimentação (Entrada/Saída)
        frame_mov = QFrame()
        frame_mov.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #d1c9b8;")
        layout_mov = QHBoxLayout(frame_mov)
        layout_mov.setContentsMargins(10, 5, 10, 5) # Margens internas menores
        
        layout_mov.addWidget(QLabel("Qtd:"))
        
        self.spin_qtd_mov = QSpinBox()
        self.spin_qtd_mov.setMinimum(1)
        self.spin_qtd_mov.setMaximum(10000)
        self.spin_qtd_mov.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px; background: #f9f9f9;")
        layout_mov.addWidget(self.spin_qtd_mov)
        
        layout_mov.addWidget(QLabel("Obs:"))
        
        self.txt_obs_mov = QLineEdit()
        self.txt_obs_mov.setPlaceholderText("Motivo...")
        self.txt_obs_mov.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px; background: #f9f9f9; min-width: 150px;")
        layout_mov.addWidget(self.txt_obs_mov)
        
        # Botões Verde (Entrada) e Vermelho (Saída)
        btn_entrada = self.criar_botao_acao("Entrada", "#10B981", self.registrar_entrada)
        btn_saida = self.criar_botao_acao("Saída", "#EF4444", self.registrar_saida)
        
        layout_mov.addWidget(btn_entrada)
        layout_mov.addWidget(btn_saida)
        
        layout_acoes.addWidget(frame_mov)
        layout_principal.addLayout(layout_acoes)

        # 5. TABELA
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7) 
        self.tabela.setHorizontalHeaderLabels(["ID", "Fotos", "Nome", "Qtd", "Min", "Localização", "Caixa"])

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Define a largura da coluna da FOTO (Coluna 1) para 100 pixels (para ficar quadrada)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.tabela.setColumnWidth(1, 100)    

        self.tabela.setColumnHidden(0, True) 
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Bloqueia a edição com duplo clique
        self.tabela.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
        
        self.tabela.setStyleSheet("""
            QHeaderView::section { 
                background-color: #e8e0cc; 
                color: #1F2937; 
                font-weight: bold; 
                border: 1px solid #d1c9b8; 
            }
            QTableWidget { 
                background-color: white; 
                color: #1F2937; 
                gridline-color: #d1c9b8;
                outline: 0; 
            }
            QTableWidget::item:selected {
                background-color: #a39179;
                color: #1F2937;
                border: none;
            }
        """)
        
        layout_principal.addWidget(self.tabela)
        self.setLayout(layout_principal)
        self.carregar_itens()

    def criar_cartao(self, layout, titulo):
        card = QFrame()
        card.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #d1c9b8;")
        c_layout = QVBoxLayout(card)
        lbl_t = QLabel(titulo); lbl_t.setStyleSheet("color: #6B7280; font-size: 11px; font-weight: bold; border: none;")
        lbl_v = QLabel("0"); lbl_v.setStyleSheet("color: #1E3A8A; font-size: 20px; font-weight: bold; border: none;")
        c_layout.addWidget(lbl_t); c_layout.addWidget(lbl_v)
        layout.addWidget(card)
        return lbl_v

    def criar_botao_acao(self, texto, cor, funcao):
        btn = QPushButton(texto)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"background-color: {cor}; color: white; border-radius: 5px; padding: 10px 18px; font-weight: bold;")
        btn.clicked.connect(funcao)
        return btn

    def limpar_filtros(self):
        self.txt_filtro_nome.clear()
        self.txt_filtro_local.clear()
        self.txt_filtro_caixa.clear()
        self.carregar_itens()

    def carregar_itens(self):
        """Busca itens com filtros e atualiza todos os cartões, incluindo movimentações do dia"""
        if not os.path.exists(self.caminho_db):
            return

        conn = sqlite3.connect(self.caminho_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # --- 1. LÓGICA DE BUSCA DE ITENS (Sua lógica atual) ---
            cursor.execute("PRAGMA table_info(itens)")
            colunas = [col[1].lower() for col in cursor.fetchall()]
            
            col_nome = 'nome' if 'nome' in colunas else colunas[1]
            col_local = 'localizacao' if 'localizacao' in colunas else (colunas[4] if len(colunas) > 4 else None)
            col_caixa = 'caixa' if 'caixa' in colunas else ('categoria' if 'categoria' in colunas else None)
            
            f_nome = f"%{self.txt_filtro_nome.text()}%"
            f_local = f"%{self.txt_filtro_local.text()}%"
            f_caixa = f"%{self.txt_filtro_caixa.text()}%"

            query = f"SELECT * FROM itens WHERE {col_nome} LIKE ?"
            params = [f_nome]
            if col_local:
                query += f" AND {col_local} LIKE ?"
                params.append(f_local)
            if col_caixa:
                query += f" AND {col_caixa} LIKE ?"
                params.append(f_caixa)

            cursor.execute(query, params)
            dados = cursor.fetchall()
            
            self.tabela.setRowCount(0)
            total_unidades = 0
            baixo_estoque = 0
            
            for row_idx, row in enumerate(dados):
                self.tabela.insertRow(row_idx)
                self.tabela.setRowHeight(row_idx, 100) 

                # Cores e Quantidades
                try: qtd = int(row['quantidade'])
                except: qtd = 0
                try: min_q = int(row['quantidade_minima'])
                except: min_q = 0

                cor_fundo = QColor("#FFDADA") if qtd <= min_q else QColor("white")

                # Preenchimento da Tabela
                item_id = QTableWidgetItem(str(row[0]))
                item_id.setBackground(cor_fundo)
                self.tabela.setItem(row_idx, 0, item_id)

                # Foto (Usando QLabel para evitar o azul)
                label_foto = QLabel()
                label_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label_foto.setStyleSheet(f"background-color: {cor_fundo.name()}; border: none;")
                if 'foto' in colunas and row['foto']:
                    caminho_c = os.path.join(self.pasta_fotos, row['foto'])
                    if os.path.exists(caminho_c):
                        pixmap = QPixmap(caminho_c).scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        label_foto.setPixmap(pixmap)
                self.tabela.setCellWidget(row_idx, 1, label_foto)

                # Demais Colunas
                cols_mapping = {2: col_nome, 3: 'quantidade', 4: 'quantidade_minima', 5: col_local, 6: col_caixa}
                for col_idx, col_name in cols_mapping.items():
                    val = str(row[col_name]) if col_name and row[col_name] is not None else ""
                    item = QTableWidgetItem(val)
                    item.setBackground(cor_fundo)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter if col_idx != 2 else Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                    
                    if col_idx == 2 and qtd <= min_q:
                        baixo_estoque += 1
                        item.setForeground(QColor("#B91C1C"))
                        f = item.font(); f.setBold(True); item.setFont(f)
                    
                    self.tabela.setItem(row_idx, col_idx, item)
                
                total_unidades += qtd

            # --- 2. NOVA LÓGICA: CONTAR MOVIMENTAÇÕES DE HOJE ---
            hoje = datetime.now().strftime("%Y-%m-%d")
            # Busca quantas movimentações foram feitas hoje
            cursor.execute("SELECT COUNT(*) FROM movimentacoes WHERE data LIKE ?", (f"{hoje}%",))
            total_mov_hoje = cursor.fetchone()[0]

            # --- 3. ATUALIZAR OS CARTÕES ---
            self.lbl_total_itens.setText(str(len(dados)))
            self.lbl_unidades.setText(str(total_unidades))
            self.lbl_estoque_baixo.setText(str(baixo_estoque))
            self.lbl_movimentacoes.setText(str(total_mov_hoje)) # <--- Agora funciona!

        except Exception as e:
            print(f"❌ Erro ao carregar: {e}")
        finally:
            conn.close()

    # MÉTODOS DE AÇÃO
    def editar_selecionado(self):
        linha = self.tabela.currentRow()
        if linha >= 0:
            self.callback_editar(self.tabela.item(linha, 0).text())
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um item!")

    def deletar_item(self):
        linha = self.tabela.currentRow()
        if linha < 0: return
        
        item_id = self.tabela.item(linha, 0).text()
        if QMessageBox.question(self, "Excluir", "Deseja apagar este item?") == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect(self.caminho_db)
            conn.cursor().execute("DELETE FROM itens WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            self.carregar_itens()

    def registrar_entrada(self):
        self._processar_movimentacao("ENTRADA")

    def registrar_saida(self):
        self._processar_movimentacao("SAÍDA")

    def _processar_movimentacao(self, tipo):
        linha = self.tabela.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um item na tabela primeiro!")
            return

        # Pega os valores da interface
        qtd_movimento = self.spin_qtd_mov.value()
        observacao = self.txt_obs_mov.text()

        # Dados da linha selecionada
        item_id_valor = self.tabela.item(linha, 0).text() # id_item
        nome_item = self.tabela.item(linha, 2).text()
        
        try:
            qtd_atual = int(self.tabela.item(linha, 3).text())
        except:
            qtd_atual = 0

        # Normaliza o tipo para o banco (remove acento para bater com o CHECK da sua tabela)
        # Na sua tabela está: CHECK(tipo IN ('ENTRADA','SAIDA'))
        tipo_db = "SAIDA" if "SAÍ" in tipo.upper() else "ENTRADA"

        # Validação de estoque para saída
        if tipo_db == "SAIDA" and qtd_movimento > qtd_atual:
            QMessageBox.critical(self, "Erro", f"Estoque insuficiente de '{nome_item}'!\nSaldo atual: {qtd_atual}")
            return

        # Calcula nova quantidade
        nova_qtd = (qtd_atual + qtd_movimento) if tipo_db == "ENTRADA" else (qtd_atual - qtd_movimento)
        data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(self.caminho_db)
        cursor = conn.cursor()
        
        try:
            # 1. Atualizar a tabela 'itens'
            # Usando os nomes exatos: id_item e quantidade
            cursor.execute("""
                UPDATE itens 
                SET quantidade = ? 
                WHERE id_item = ?
            """, (nova_qtd, item_id_valor))

            # 2. Registrar na tabela 'movimentacoes'
            # Usando os nomes exatos da sua função create_tables:
            # id_item, id_usuario, tipo, quantidade, observacao, data
            cursor.execute("""
                INSERT INTO movimentacoes (id_item, id_usuario, tipo, quantidade, observacao, data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (item_id_valor, self.usuario_id, tipo_db, qtd_movimento, observacao, data_hora_atual))

            conn.commit()
            
            # Limpa os campos de entrada após o sucesso
            self.spin_qtd_mov.setValue(1)
            self.txt_obs_mov.clear()
            
            # Recarrega a visualização
            self.carregar_itens()
            
            # Mantém a linha selecionada para facilitar o trabalho
            self.tabela.selectRow(linha)
            
            # Feedback visual (opcional, pode remover se achar irritante)
            # print(f"✅ {tipo_db} de {qtd_movimento} unidades de {nome_item} realizada.")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Erro", f"Falha ao salvar no banco de dados: {e}")
        finally:
            conn.close()