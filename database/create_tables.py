from database.connection import connect

def create_tables():

    conn = connect()
    cursor = conn.cursor()

    # ATUALIZADO: Adicionada coluna 'foto' TEXT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nivel TEXT,
        foto TEXT 
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        foto TEXT,
        caixa TEXT,
        localizacao TEXT,
        quantidade INTEGER,
        quantidade_minima INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_item INTEGER,
        id_usuario INTEGER,
        tipo TEXT CHECK(tipo IN ('ENTRADA','SAIDA')),
        quantidade INTEGER,
        observacao TEXT,
        data DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(id_item) REFERENCES itens(id_item),
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
    )
    """)

    conn.commit()
    conn.close()
    print("Tabelas criadas/atualizadas com sucesso.")

if __name__ == "__main__":
    create_tables()