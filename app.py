from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

def init_db():
    conn = sqlite3.connect('personagem.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personagem 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nome TEXT, nascimento TEXT, idade INTEGER, 
                  funcao TEXT, nivel TEXT, genero TEXT)''')
    conn.commit()
    conn.close()

@app.route('/personagem', methods=['GET'])
def listar_personagens():
    """
    Lista todos os personagens.
    ---
    responses:
      200:
        description: Retorna a lista de personagens.
    """
    conn = sqlite3.connect('personagem.db')
    c = conn.cursor()
    c.execute('SELECT * FROM personagem')
    linhas = c.fetchall()
    personagens = []
    for row in linhas:
        personagens.append({
            'id': row[0], 'nome': row[1], 'nascimento': row[2], 
            'idade': row[3], 'funcao': row[4], 'nivel': row[5], 'genero': row[6]
        })
    conn.close()
    return jsonify(personagens)

@app.route('/personagem', methods=['POST'])
def adicionar_personagem():
    """
    Cadastra um novo personagem.
    ---
    responses:
      201:
        description: Sucesso.
    """
    novo = request.json
    if not novo.get('nome') or not novo.get('genero'):
        return jsonify({'erro': 'Nome e gênero são obrigatórios!'}), 400
        
    conn = sqlite3.connect('personagem.db')
    c = conn.cursor()
    c.execute('''INSERT INTO personagem (nome, nascimento, idade, funcao, nivel, genero) 
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (novo['nome'], novo['nascimento'], novo['idade'], novo['funcao'], novo['nivel'], novo['genero']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Personagem cadastrado com sucesso!'}), 201

@app.route('/personagem/<int:id>', methods=['PUT'])
def atualizar_personagem(id):
    """
    Atualiza um personagem.
    ---
    responses:
      200:
        description: Sucesso.
    """
    dados = request.json
    conn = sqlite3.connect('personagem.db')
    c = conn.cursor()
    c.execute('''UPDATE personagem 
                 SET nome = ?, nascimento = ?, idade = ?, funcao = ?, nivel = ?, genero = ? 
                 WHERE id = ?''', 
              (dados['nome'], dados['nascimento'], dados['idade'], dados['funcao'], dados['nivel'], dados['genero'], id))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Personagem atualizado!'})

@app.route('/personagem/<int:id>', methods=['DELETE'])
def excluir_personagem(id):
    """
    Exclui um personagem.
    ---
    responses:
      200:
        description: Sucesso.
    """
    conn = sqlite3.connect('personagem.db')
    c = conn.cursor()
    c.execute('DELETE FROM personagem WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Personagem excluído!'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)