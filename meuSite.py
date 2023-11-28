#importar dependencias necessarias

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# inicializar o site e configurar o db
app = Flask(__name__) # cria uma instancia do app flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.sqlite3' # indica a conexao do app com o banco de dados sqlite
db = SQLAlchemy(app) # cria uma variavel de conexao com o banco 

# criar o model da tabela 
class Usuario(db.Model):
    id = db.Column('id',db.Integer, primary_key = True,autoincrement = True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150))
    
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email



# definir a rota de listar os usuarios
@app.route('/')
def listarUsuarios():
    db.create_all()
    usuarios = Usuario.query.all()
    return {"usuarios": [{"id": usuario.id, "nome": usuario.nome, "email": usuario.email} for usuario in usuarios]}


#definir a rota de adicionar um usuario

@app.route('/addUsuario', methods=['GET', 'POST'])
def addUsuario():
    if request.method == 'POST':
        nome = request.json.get("nome")
        email = request.json.get("email")
        novo_usuario = Usuario(nome=nome, email=email)
        db.session.add(novo_usuario)
        db.session.commit()

        return {"mensagem": "Usuário adicionado com sucesso."}

    return {"mensagem": "Rota acessada via GET. Use POST para adicionar um usuário."}


# definir a rota para deletar um usuario
@app.route('/deletarUsuario', methods=['POST'])
def deletarUsuario():
    usuario_id = request.json.get("id")
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return {"mensagem": f"Usuário com ID {usuario_id} deletado com sucesso."}
    else:
        return {"mensagem": f"Usuário com ID {usuario_id} não encontrado."}

#definir rota para editar um usuario

@app.route('/alterarUsuario', methods=['GET', 'POST'])
def alterarUsuario():
    if(request.method == 'POST'):
        usuario_id = request.json.get('id')
        usuario_nome = request.json.get('nome')
        usuario_email = request.json.get('email')

        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.nome = usuario_nome
            usuario.email = usuario_email
            db.session.commit()
            return {"mensagem": f"Usuário com ID {usuario_id} alterado com sucesso."}
        else:
            return {"mensagem": f"Usuário com ID {usuario_id} não encontrado"}


if __name__ == '__main__':
    app.run(debug=True)
