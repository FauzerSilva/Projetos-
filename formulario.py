from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

# Função para salvar dados no PostgreSQL
def salvar_dados(desenvolvedor, projeto, empresa, data, horas_semana):
    # Conexão com o banco de dados (os dados de conexão virão das variáveis de ambiente)
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", 5432)
    )
    cursor = conn.cursor()

    # Criar a tabela se ela ainda não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id SERIAL PRIMARY KEY,
            desenvolvedor VARCHAR(255),
            projeto VARCHAR(255),
            empresa VARCHAR(255),
            data DATE,
            horas_semana INT
        )
    """)

    # Inserir os dados no banco
    cursor.execute("""
        INSERT INTO respostas (desenvolvedor, projeto, empresa, data, horas_semana)
        VALUES (%s, %s, %s, %s, %s)
    """, (desenvolvedor, projeto, empresa, data, horas_semana))

    conn.commit()  # Salvar as alterações no banco
    cursor.close()
    conn.close()

@app.route('/')
def formulario():
    return '''
    <form action="/enviar" method="post">
        <label>Desenvolvedor:</label><br>
        <input type="text" name="desenvolvedor" required><br><br>
        
        <label>Projeto:</label><br>
        <input type="text" name="projeto" required><br><br>

        <label>Empresa:</label><br>
        <input type="text" name="empresa" required><br><br>

        <label>Data:</label><br>
        <input type="date" name="data" required><br><br>

        <label>Quantidade de horas:</label><br>
        <input type="number" name="quantidade_de_horas" required><br><br>

        <button type="submit">Enviar</button>
    </form>
    '''

@app.route('/enviar', methods=['POST'])
def enviar():
    desenvolvedor = request.form['desenvolvedor']
    projeto = request.form['projeto']
    empresa = request.form['empresa']
    data = request.form["data"]
    horas_semana = request.form["quantidade_de_horas"]
    salvar_dados(desenvolvedor, projeto, empresa, data, horas_semana)
    return "Dados enviados com sucesso!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
