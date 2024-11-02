import oracledb
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000", "http://localhost:3000"])

def get_conexao():
    return oracledb.connect(user='seu_usuario', password='sua_senha',
                            dsn='dsn_do_seu_banco_oracle')

@app.route('/login', methods=['POST'])
def recupera_login():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({'error': 'Email and password are required'}), 400

        with get_conexao() as conexao:
            with conexao.cursor() as cursor:
                sql = 'SELECT ds_email FROM T_SLC_CLIENTE WHERE ds_email = :email AND ds_senha = :senha'
                cursor.execute(sql, {'email': email, 'senha': senha})
                reg = cursor.fetchone()
                if reg:
                    return jsonify({'message': 'Login successful', 'email': reg[0]}), 200
                else:
                    return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
