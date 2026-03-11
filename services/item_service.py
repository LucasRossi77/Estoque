from database.connection import connect

def listar_itens():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM itens")

    itens = cursor.fetchall()

    conn.close()

    return itens


def adicionar_item(nome, caixa, localizacao, quantidade, quantidade_minima, foto):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO itens (nome, caixa, localizacao, quantidade, quantidade_minima, foto)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, caixa, localizacao, quantidade, quantidade_minima, foto))

    conn.commit()
    conn.close()