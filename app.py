from flask import Flask, request, redirect, send_from_directory
import mysql.connector
import os

app = Flask(__name__, static_folder='.', static_url_path='')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def get_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='instagram_like',
        user='kesar',
        password='1234'
    )

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/save', methods=['POST'])
def save():
    identifier = request.form.get('identifier', '')
    password   = request.form.get('password', '')

    db  = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO utilisateurs (identifier, mot_de_passe) VALUES (%s, %s)", (identifier, password))
    db.commit()
    cur.close()
    db.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)