from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicas.sqlite3'
db = SQLAlchemy(app)

class Musica(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nome = db.Column(db.String(150), nullable=False)
   artista = db.Column(db.String(150), nullable=False)
   link = db.Column(db.String(300), nullable=False)

   def __init__(self, nome, artista, link):
      self.nome = nome
      self.artista = artista
      self.link = link

@app.route('/')
def index():
   musicas = Musica.query.all()
   return render_template('index.html', musicas=musicas)

@app.route('/<id>')
def musica_pelo_id(id):
   musica = Musica.query.get(id)
   return render_template('index.html', musica=musica)

@app.route('/new', methods=['GET', 'POST'])
def new():
   if request.method == 'POST':
      musica = Musica(
         request.form['nome'],
         request.form['artista'],
         request.form['link']
      )
      db.session.add(musica)
      db.session.commit()
      return redirect('/#playlist')
   return render_template('new.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
   musica = Musica.query.get(id)
   if request.method == "POST":
      musica.nome = request.form['nome']
      musica.artista = request.form['artista']
      musica.link = request.form['link']
      db.session.commit()
      return redirect('/#playlist')
   return render_template('edit.html', musica=musica)

@app.route('/delete/<id>')
def delete(id):
   musica = Musica.query.get(id)
   db.session.delete(musica)
   db.session.commit()
   return redirect('/#playlist')

if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)