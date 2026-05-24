# Sistema de Reconhecimento Facial

Sistema web desenvolvido para a empresa fictícia FaceID Security, capaz de identificar pessoas automaticamente através de imagens ou câmera ao vivo.

## Tecnologias Utilizadas

- Python 3.11
- Flask
- OpenCV
- face_recognition
- dlib 19.24.1
- SQLite
- HTML5, CSS3, JavaScript
- Bootstrap 5

## Funcionalidades

### Obrigatórias
- Cadastro de pessoas com múltiplas fotos faciais
- Reconhecimento facial via webcam em tempo real
- Reconhecimento facial via upload de imagem
- Lista de pessoas cadastradas
- Banco de dados com tabelas pessoas e imagens

### Extras
- Histórico de reconhecimentos
- Marcação facial com quadrado verde
- Login administrativo (usuário: admin / senha: admin123)

## Como Executar

### 1. Clone o repositório
    git clone https://github.com/NewSantos-art/sistema-reconhecimento-facial.git
cd sistema-reconhecimento-facial

### 2. Crie o ambiente virtual com Python 3.11
    py -3.11 -m venv venv

### 3. Ative o ambiente virtual
    venv\Scripts\activate

### 4. Instale o cmake
    pip install cmake

### 5. Instale o dlib manualmente 
    Baixe o arquivo e coloque na pasta do projeto:
    https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.1-cp311-cp311-win_amd64.whl
    Depois instale:
    pip install dlib-19.24.1-cp311-cp311-win_amd64.whl

### 6. Instale as demais dependências
    pip install -r requirements.txt

### 7. Execute o servidor
    python backend/app.py

### 8. Acesse no navegador
    http://127.0.0.1:5000

## Estrutura do Projeto

faceid-system/
├── backend/
│   ├── app.py
│   ├── database.py
│   └── uploads/
├── frontend/
│   ├── index.html
│   ├── cadastro.html
│   ├── webcam.html
│   ├── imagem.html
│   ├── pessoas.html
│   ├── historico.html
│   ├── login.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── cadastro.js
│       ├── webcam.js
│       ├── imagem.js
│       ├── pessoas.js
│       ├── historico.js
│       └── login.js
├── requirements.txt
└── README.md

## Autor

NewSantos-art