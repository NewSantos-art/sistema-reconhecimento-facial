from flask import Flask, jsonify, request
from flask import send_from_directory
from flask_cors import CORS
import database
import os

app = Flask(__name__)
CORS(app)
os.makedirs('backend/uploads', exist_ok=True)

database.criar_tabela()

@app.route('/pessoas', methods=['GET'])
def listar_pessoas():
    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pessoas')
    pessoas = cursor.fetchall()
    conn.close()

    resultado = []
    for pessoa in pessoas:
        resultado.append({
            'id': pessoa[0],
            'nome': pessoa[1],
            'cpf': pessoa[2],
            'data_cadastro': pessoa[3]
        })

    return jsonify(resultado)

@app.route('/pessoas', methods=['POST'])
def cadastrar_pessoa():
    dados = request.get_json()
    nome = dados.get('nome')
    cpf = dados.get('cpf')

    if not nome or not cpf:
        return jsonify({'error': 'Nome e CPF são obrigatórios'}), 400

    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pessoas (nome, cpf) VALUES (?, ?)', (nome, cpf))
    conn.commit()
    pessoa_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Pessoa cadastrada com sucesso', 'id': pessoa_id}), 201

@app.route('/imagem/<int:pessoa_id>', methods=['POST'])
def upload_imagem(pessoa_id):
    if 'imagem' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    imagem = request.files['imagem']
    caminho_imagem = f'backend/uploads/{pessoa_id}_{imagem.filename}'
    imagem.save(caminho_imagem)

    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO imagens (pessoa_id, caminho_imagem) VALUES (?, ?)', (pessoa_id, caminho_imagem))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Imagem cadastrada com sucesso'}), 201

@app.route('/pessoas/<int:pessoa_id>', methods=['GET'])
def buscar_pessoa(pessoa_id):
    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pessoas WHERE id = ?', (pessoa_id,))
    pessoa = cursor.fetchone()
    conn.close()

    if pessoa:
        return jsonify({
            'id': pessoa[0],
            'nome': pessoa[1],
            'cpf': pessoa[2],
            'data_cadastro': pessoa[3]
        })
    else:
        return jsonify({'error': 'Pessoa não encontrada'}), 404

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
