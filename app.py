from flask import Flask, render_template, request, redirect, url_for, session
from models import Paciente, Maqueiro, SistemaTransporte, SolicitacaoTransporte

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Usuário único para simplificação
USUARIO = 'admin'
SENHA = 'maqueiro'

# Inicialização do sistema de transporte
sistema_transporte = SistemaTransporte()

# Maqueiro teste
maqueiro = Maqueiro(1, "Anacleto Costa")

# Pacientes teste
paciente1 = Paciente(1, "Gilvanderson de Lima", "Sala 141")
paciente2 = Paciente(2, "Rayllany Pereira", "Sala 53")

# Adicionar solicitações de exemplo
sistema_transporte.criar_solicitacao(paciente1, "Alta")
sistema_transporte.criar_solicitacao(paciente2, "Média")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USUARIO and password == SENHA:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/solicitacoes')
def listar_solicitacoes():
    if 'logged_in' in session:
        return render_template('solicitacoes.html', solicitacoes=sistema_transporte.solicitacoes)
    else:
        return redirect(url_for('login'))

@app.route('/aceitar/<int:id_solicitacao>')
def aceitar_solicitacao(id_solicitacao):
    if 'logged_in' in session:
        maqueiro.aceitar_solicitacao(id_solicitacao, sistema_transporte)
        return redirect(url_for('listar_solicitacoes'))
    else:
        return redirect(url_for('login'))

@app.route('/recusar/<int:id_solicitacao>')
def recusar_solicitacao(id_solicitacao):
    if 'logged_in' in session:
        maqueiro.recusar_solicitacao(id_solicitacao, sistema_transporte)
        return redirect(url_for('listar_solicitacoes'))
    else:
        return redirect(url_for('login'))

@app.route('/incidente/<int:id_solicitacao>', methods=['GET', 'POST'])
def registrar_incidente(id_solicitacao):
    if 'logged_in' in session:
        if request.method == 'POST':
            descricao = request.form['descricao']
            maqueiro.registrar_incidente(id_solicitacao, descricao, sistema_transporte)
            return redirect(url_for('listar_solicitacoes'))
        return render_template('incidente.html', id_solicitacao=id_solicitacao)
    else:
        return redirect(url_for('login'))

@app.route('/chegou/<int:id_solicitacao>')
def chegou_ao_destino(id_solicitacao):
    if 'logged_in' in session:
        maqueiro.chegou_ao_destino(id_solicitacao, sistema_transporte)
        return redirect(url_for('listar_solicitacoes'))
    else:
        return redirect(url_for('login'))

@app.route('/adicionar_solicitacao', methods=['GET', 'POST'])
def adicionar_solicitacao():
    if 'logged_in' in session:
        if request.method == 'POST':
            nome_paciente = request.form['nome_paciente']
            localizacao = request.form['localizacao']
            prioridade = request.form['prioridade']
            id_paciente = len(sistema_transporte.solicitacoes) + 1
            paciente = Paciente(id_paciente, nome_paciente, localizacao)
            sistema_transporte.criar_solicitacao(paciente, prioridade)
            return redirect(url_for('listar_solicitacoes'))
        return render_template('adicionar_solicitacao.html')
    else:
        return redirect(url_for('login'))

@app.route('/remover/<int:id_solicitacao>')
def remover_solicitacao(id_solicitacao):
    if 'logged_in' in session:
        sistema_transporte.remover_solicitacao(id_solicitacao)
        return redirect(url_for('listar_solicitacoes'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
