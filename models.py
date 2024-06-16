class Paciente:
    def __init__(self, id, nome, localizacao):
        self.id = id
        self.nome = nome
        self.localizacao = localizacao

class Maqueiro:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def aceitar_solicitacao(self, id_solicitacao, sistema_transporte):
        for solicitacao in sistema_transporte.solicitacoes:
            if solicitacao.id == id_solicitacao:
                solicitacao.aceitar()

    def recusar_solicitacao(self, id_solicitacao, sistema_transporte):
        for solicitacao in sistema_transporte.solicitacoes:
            if solicitacao.id == id_solicitacao:
                solicitacao.recusar()

    def registrar_incidente(self, id_solicitacao, descricao, sistema_transporte):
        for solicitacao in sistema_transporte.solicitacoes:
            if solicitacao.id == id_solicitacao:
                solicitacao.registrar_incidente(descricao)

    def chegou_ao_destino(self, id_solicitacao, sistema_transporte):
        for solicitacao in sistema_transporte.solicitacoes:
            if solicitacao.id == id_solicitacao:
                solicitacao.chegou_ao_destino()

class SistemaTransporte:
    def __init__(self):
        self.solicitacoes = []

    def criar_solicitacao(self, paciente, prioridade):
        id_solicitacao = len(self.solicitacoes) + 1
        solicitacao = SolicitacaoTransporte(id_solicitacao, paciente, prioridade)
        self.solicitacoes.append(solicitacao)

    def registrar_incidente(self, id_solicitacao, descricao):
        for solicitacao in self.solicitacoes:
            if solicitacao.id == id_solicitacao:
                solicitacao.registrar_incidente(descricao)

    def remover_solicitacao(self, id_solicitacao):
        self.solicitacoes = [solicitacao for solicitacao in self.solicitacoes if solicitacao.id != id_solicitacao]

class SolicitacaoTransporte:
    def __init__(self, id, paciente, prioridade):
        self.id = id
        self.paciente = paciente
        self.prioridade = prioridade
        self.status = "Aguardando transporte"
        self.incidentes = []

    def aceitar(self):
        self.status = "Em transporte"

    def recusar(self):
        self.status = "Recusada"

    def registrar_incidente(self, descricao):
        self.incidentes.append(descricao)

    def chegou_ao_destino(self):
        self.status = "Chegou ao destino"
