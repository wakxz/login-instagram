from flask import Flask, request, redirect, send_from_directory
import mysql.connector
import os

app = Flask(__name__, static_folder='.', static_url_path='')

def get_db():
    return mysql.connector.connect(
        host=os.environ.get('MYSQLHOST'),
        port=int(os.environ.get('MYSQLPORT', 3306)),
        database=os.environ.get('MYSQLDATABASE'),
        user=os.environ.get('MYSQLUSER'),
        password=os.environ.get('MYSQLPASSWORD')
    )

@app.route('/')
def index():
    return app.send_static_file('main.html')

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