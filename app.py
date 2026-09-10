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

@app.route('/personagens', methods=['GET'])
def listar_personagens():
    """
    Lista todos os personagens cadastrados.
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

@app.route('/personagens', methods=['POST'])
def adicionar_personagem():
    """
    Cadastra um novo personagem.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
            - genero
          properties:
            nome:
              type: string
              example: "Lara Croft"
            nascimento:
              type: string
              example: "14/02/1992"
            idade:
              type: integer
              example: 31
            funcao:
              type: string
              example: "Arqueóloga"
            nivel:
              type: string
              example: "Avançado"
            genero:
              type: string
              example: "Feminino"
    responses:
      201:
        description: Personagem cadastrado com sucesso.
      400:
        description: Erro de validação.
    """
    novo = request.json
    if not novo.get('nome') or not novo.get('genero'):
        return jsonify({'erro': 'Nome e gênero são obrigatórios!'}), 400
        
    conn = sqlite3.connect('personagem.db')
    c = conn.cursor()
    c.execute('''INSERT INTO personagem (nome, nascimento, idade, funcao, nivel, genero) 
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (novo['nome'], novo.get('nascimento'), novo.get('idade'), novo.get('funcao'), novo.get('nivel'), novo['genero']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Personagem cadastrado com sucesso!'}), 201

@app.route('/personagens/<int:id>', methods=['PUT'])
def atualizar_personagem(id):
    """
    Atualiza os dados de um personagem.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do personagem a ser atualizado.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Lara Croft"
            nascimento:
              type: string
              example: "14/02/1992"
            idade:
              type: integer
              example: 32
            funcao:
              type: string
              example: "Aventureira"
            nivel:
              type: string
              example: "Mestre"
            genero:
              type: string
              example: "Feminino"
    responses:
      200:
        description: Personagem atualizado com sucesso.
    """
    dados = request.json
    conn = sqlite3.connect('personagem.db')
    c = conn.cursor()
    c.execute('''UPDATE personagem 
                 SET nome = ?, nascimento = ?, idade = ?, funcao = ?, nivel = ?, genero = ? 
                 WHERE id = ?''', 
              (dados['nome'], dados.get('nascimento'), dados.get('idade'), dados.get('funcao'), dados.get('nivel'), dados['genero'], id))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Personagem atualizado!'})

@app.route('/personagens/<int:id>', methods=['DELETE'])
def excluir_personagem(id):
    """
    Exclui um personagem do banco de dados.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do personagem a ser excluído.
    responses:
      200:
        description: Personagem excluído com sucesso.
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