from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'imagens')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn= sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imagens(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caminho TEXT NOT NULL,
            descricao TEXT NOT NULL
            )
    ''')
    conn.commit()
    conn.close()
     
init_db()

@app.route('/')
def index():
    conn= sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT caminho, descricao, id FROM imagens")
    imagens = cursor.fetchall()
    conn.close()
    return render_template('index.html', imagens=imagens)

@app.route("/ongs", methods=["GET", "POST"])
def cadastra_ong():
    if request.method == "POST":  
        descricao = request.form["descricao"] 
        imagem = request.files["imagem"]  

        if imagem:
            filename = secure_filename(imagem.filename) 
            caminho = os.path.join(UPLOAD_FOLDER, filename) 
            caminho = caminho.replace('\\', '/') 
            imagem.save(caminho) 

            conn = sqlite3.connect('database.db') 
            c = conn.cursor()
            c.execute("INSERT INTO imagens (caminho, descricao) VALUES (?, ?)",
                      (caminho, descricao))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))  
    return render_template("cadastra-ong.html")

@app.route("/delete/<int:imagem_id>", methods=["POST"])
def delete(imagem_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT caminho FROM imagens WHERE id = ?", (imagem_id,))
    imagem = c.fetchone()
    
    if imagem:
        caminho = imagem[0]
        if os.path.exists(caminho):  
            os.remove(caminho)
        c.execute("DELETE FROM imagens WHERE id = ?", (imagem_id,))
        conn.commit()

    conn.close()
    return redirect(url_for('index'))

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/ajuda")
def ajuda():
    return render_template("ajuda.html")

if __name__ == '__main__':
    app.run(debug=True)