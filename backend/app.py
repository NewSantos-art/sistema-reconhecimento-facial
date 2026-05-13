from flask import Flask, jsonify, request
from flask import send_from_directory
from flask_cors import CORS
from PIL import Image
import numpy as np
import face_recognition
import database
import uuid
import cv2
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
    caminho_imagem = f'backend/uploads/{pessoa_id}_{uuid.uuid4().hex}_{imagem.filename}'
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

@app.route('/<path:filename>')
def frontend(filename):
    return send_from_directory('../frontend', filename)

@app.route('/reconhecer', methods=['POST'])
def reconhecer():
    try:
        if 'imagem' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400

        imagem_enviada = request.files['imagem']
        caminho_temp = os.path.join(os.path.dirname(__file__), 'uploads', 'temp_reconhecimento.jpg')
        imagem_enviada.save(caminho_temp)

        img_pil = Image.open(caminho_temp).convert('RGB')
        img_pil = img_pil.resize((640, 480))
        imagem = np.ascontiguousarray(np.array(img_pil, dtype=np.uint8))
        locations = face_recognition.face_locations(imagem, number_of_times_to_upsample=2)
        encodings_enviados = face_recognition.face_encodings(imagem, locations)
        
        if len(encodings_enviados) == 0:
            return jsonify({'error': 'Nenhum rosto detectado na imagem'})

        encoding_enviado = encodings_enviados[0]

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT pessoa_id, caminho_imagem FROM imagens')
        imagens_cadastradas = cursor.fetchall()
        conn.close()

        melhor_match = None
        melhor_distancia = 1.0

        metodo = request.form.get('metodo', 'imagem')

        for pessoa_id, caminho in imagens_cadastradas:
            try:
                img_pil_cad = Image.open(caminho).convert('RGB')
                img_pil_cad = img_pil_cad.resize((640, 480))
                img_cadastrada = np.ascontiguousarray(np.array(img_pil_cad, dtype=np.uint8))
                locs_cadastradas = face_recognition.face_locations(img_cadastrada, number_of_times_to_upsample=2)
                encodings_cadastrados = face_recognition.face_encodings(img_cadastrada, locs_cadastradas)
                if len(encodings_cadastrados) == 0:
                    continue
                distancia = face_recognition.face_distance([encodings_cadastrados[0]], encoding_enviado)[0]
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_match = pessoa_id
            except Exception as e:
                print(f"Erro ao processar imagem {caminho}: {str(e)}")
                continue
        
        conn = database.conectar()
        cursor = conn.cursor()
        if melhor_match is None or melhor_distancia > 0.6:
            conn = database.conectar()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO historico (pessoa_id, nome, confianca, metodo)
                VALUES (?, ?, ?, ?)''', (None, 'Desconhecido', '0%', metodo))
            conn.commit()
            conn.close()
            return jsonify({'resultado': 'Pessoa não identificada'})

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pessoas WHERE id = ?', (melhor_match,))
        pessoa = cursor.fetchone()
        conn.close()

        confianca = round((1 - melhor_distancia) * 100, 2)

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO historico (pessoa_id, nome, confianca, metodo)
            VALUES (?, ?, ?, ?)''', (pessoa[0], pessoa[1], f'{confianca}%', metodo))
        conn.commit()
        conn.close()

        return jsonify({
            'resultado': 'Pessoa identificada',
            'nome': pessoa[1],
            'id': pessoa[0],
            'confianca': f'{confianca}%'
        })

    except Exception as e:
        print(f"Erro no reconhecimento: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/historico', methods=['GET'])
def listar_historico():
    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico ORDER BY data_hora DESC')
    registros = cursor.fetchall()
    conn.close()

    resultado = []
    for r in registros:
        resultado.append({
            'id': r[0],
            'pessoa_id': r[1],
            'nome': r[2],
            'confianca': r[3],
            'metodo': r[4],
            'data_hora': r[5]
        })

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
