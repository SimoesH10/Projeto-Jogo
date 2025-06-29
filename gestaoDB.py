import sqlite3 as sqlite

def criarTabelaUsuario():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            conta TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserirUsuario(nome, conta, email, senha):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, conta, email, senha) VALUES (?, ?, ?, ?)
    ''', (nome, conta, email, senha))
    conn.commit()
    conn.close()

def listarUsuarios():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, conta, email FROM usuarios ORDER BY id DESC')
    dados = cursor.fetchall()
    usuarios = []
    for row in dados:
        usuario = {
            'id': row[0],
            'nome': row[1],
            'conta': row[2],
            'email': row[3]
        }
        usuarios.append(usuario)
    conn.close()
    return usuarios


def login(email, senha):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
    dados = cursor.fetchall()
    conn.close()
    return len(dados) > 0

def verificarUsuario(email):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))  # <- corrigido com vírgula
    dados = cursor.fetchall()
    conn.close()
    return len(dados) > 0

def recuperarSenhaBD(conta, email):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE conta=? AND email=?", (conta, email))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado[0]
    return None
