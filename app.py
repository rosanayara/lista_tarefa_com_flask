from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    tarefas = Tarefa.query.order_by(Tarefa.concluida).all()
    total = Tarefa.query.count()
    feitas = Tarefa.query.filter_by(concluida=True).count()
    faltam = total - feitas
    # Calcula a porcentagem para a barra
    progresso = int((feitas / total) * 100) if total > 0 else 0
    return render_template('index.html', tarefas=tarefas, total=total, feitas=feitas, faltam=faltam, progresso=progresso)


@app.route('/adicionar', methods=['POST'])
def adicionar():
    texto = request.form.get('tarefa')
    if texto:
        db.session.add(Tarefa(conteudo=texto))
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/concluir/<int:id>')
def concluir(id):
    t = Tarefa.query.get(id)
    if t:
        t.concluida = not t.concluida
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    t = Tarefa.query.get(id)
    if request.method == 'POST':
        t.conteudo = request.form.get('tarefa')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', tarefa=t)


@app.route('/excluir/<int:id>')
def excluir(id):
    t = Tarefa.query.get(id)
    if t:
        db.session.delete(t)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/limpar_tudo')
def limpar_tudo():
    Tarefa.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)