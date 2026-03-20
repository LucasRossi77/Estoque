import sqlite3
from database.connection import connect

def autenticar_usuario(login, senha):
    conn = connect()
    cursor = conn.cursor()
    
    # Busca o usuário no banco
    cursor.execute("SELECT * FROM usuarios WHERE login = ? AND senha = ?", (login, senha))
    usuario = cursor.fetchone()
    
    conn.close()
    
    # Retorna os dados do usuário se encontrou, ou None se errou a senha
    return dict(usuario) if usuario else None

def criar_usuario_padrao():
    conn = connect()
    cursor = conn.cursor()
    
    # Verifica se a tabela está vazia
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO usuarios (nome, login, senha, nivel) 
            VALUES ('Administrador', 'admin', 'admin', 'admin')
        """)
        conn.commit()
        print("Usuário padrão criado: login 'admin', senha 'admin'")
        
    conn.close()

def registrar_usuario(nome, login, senha, nivel="usuario"):
    conn = connect()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, login, senha, nivel) 
            VALUES (?, ?, ?, ?)
        """, (nome, login, senha, nivel))
        conn.commit()
        sucesso = True
        mensagem = "Conta criada com sucesso!"
    except sqlite3.IntegrityError:
        
        sucesso = False
        mensagem = "Esse nome de usuário (login) já está em uso. Escolha outro."
    except Exception as e:
        sucesso = False
        mensagem = f"Erro ao criar usuário: {e}"
    finally:
        conn.close()
        
    return sucesso, mensagem