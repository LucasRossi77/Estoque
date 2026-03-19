from database.connection import connect
from datetime import datetime

def registrar_movimentacao(item_id, tipo, quantidade, usuario_id=None, observacao=""):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO movimentacoes
        (id_item, tipo, quantidade, id_usuario, observacao, data) -- <-- CORREÇÃO
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        item_id,
        tipo,
        quantidade,
        usuario_id,
        observacao,
        datetime.now()
    ))
    conn.commit()
    conn.close()