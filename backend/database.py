import sqlite3
from datetime import datetime

def conectar():
    conn = sqlite3.connect('backend/faceid.db')
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            cpf VARCHAR(14) NOT NULL,
            data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pessoa_id INTEGER NOT NULL,
            caminho_imagem VARCHAR(255) NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pessoa_id INTEGER,
            nome VARCHAR(100),
            confianca VARCHAR(10),
            metodo VARCHAR(20),
            data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso!")


if __name__ == "__main__":
    criar_tabela()