import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definição dos universos de discurso
x_densidade = np.arange(0, 201, 1)
x_velocidade = np.arange(0, 71, 1)
x_espera = np.arange(0, 151, 1)
x_incidentes = np.arange(0, 6.1, 0.1)
x_tempo_verde = np.arange(0, 91, 1)

# Variáveis fuzzy
densidade = ctrl.Antecedent(x_densidade, 'densidade')
velocidade = ctrl.Antecedent(x_velocidade, 'velocidade')
espera = ctrl.Antecedent(x_espera, 'espera')
incidentes = ctrl.Antecedent(x_incidentes, 'incidentes')
tempo_verde = ctrl.Consequent(x_tempo_verde, 'tempo_verde')

# Funções de pertinência
tempo_verde['curto'] = fuzz.trimf(x_tempo_verde, [0, 15, 30])
tempo_verde['medio'] = fuzz.trimf(x_tempo_verde, [20, 35, 50])
tempo_verde['longo'] = fuzz.trimf(x_tempo_verde, [40, 65, 90])

densidade['baixa'] = fuzz.trimf(x_densidade, [0, 0, 80])
densidade['media'] = fuzz.trimf(x_densidade, [50, 100, 150])
densidade['alta'] = fuzz.trimf(x_densidade, [120, 200, 200])

velocidade['baixa'] = fuzz.trimf(x_velocidade, [0, 0, 30])
velocidade['media'] = fuzz.trimf(x_velocidade, [20, 35, 50])
velocidade['alta'] = fuzz.trimf(x_velocidade, [40, 70, 70])

espera['baixa'] = fuzz.trimf(x_espera, [0, 0, 50])
espera['media'] = fuzz.trimf(x_espera, [30, 75, 120])
espera['alta'] = fuzz.trimf(x_espera, [100, 150, 150])

incidentes['baixa'] = fuzz.trimf(x_incidentes, [0, 0, 2])
incidentes['media'] = fuzz.trimf(x_incidentes, [1, 3, 5])
incidentes['alta'] = fuzz.trimf(x_incidentes, [4, 6, 6])

# Regras fuzzy
rules = []
for d in ['baixa', 'media', 'alta']:
    for v in ['baixa', 'media', 'alta']:
        for e in ['baixa', 'media', 'alta']:
            for i in ['baixa', 'media', 'alta']:
                pontos = 0
                if d == 'alta': pontos += 2
                elif d == 'media': pontos += 1
                if v == 'baixa': pontos += 2
                elif v == 'media': pontos += 1
                if e == 'alta': pontos += 2
                elif e == 'media': pontos += 1
                if i == 'alta': pontos += 2
                elif i == 'media': pontos += 1

                if pontos >= 7:
                    saida = 'longo'
                elif pontos >= 4:
                    saida = 'medio'
                else:
                    saida = 'curto'

                rule = ctrl.Rule(
                    densidade[d] & velocidade[v] & espera[e] & incidentes[i],
                    tempo_verde[saida]
                )
                rules.append(rule)

# Sistema de controle fuzzy
sistema_controle = ctrl.ControlSystem(rules)
sistema_simulacao = ctrl.ControlSystemSimulation(sistema_controle)

def calcular_tempo_fuzzy(d, v, e, i):
    """
    Calcula o tempo de verde usando o sistema fuzzy.
    """
    sistema_simulacao.input['densidade'] = d
    sistema_simulacao.input['velocidade'] = v
    sistema_simulacao.input['espera'] = e
    sistema_simulacao.input['incidentes'] = i
    sistema_simulacao.compute()
    return sistema_simulacao.output['tempo_verde']

def calcular_graus_pertinencia(tempo):
    """
    Calcula os graus de pertinência para cada categoria de tempo.
    """
    graus = {}
    for nome in tempo_verde.terms:
        mf = tempo_verde.terms[nome].mf
        grau = fuzz.interp_membership(x_tempo_verde, mf, tempo)
        graus[nome] = grau
    return graus

def gerar_explicacao(graus):
    """
    Gera explicação baseada na função dominante.
    """
    dominante = max(graus, key=graus.get)
    return f"Função dominante: {dominante.upper()} → resultado influenciado por maior pertinência nesta categoria."

def plotar_funcoes_pertinencia():
    """
    Plota as funções de pertinência do tempo de verde.
    """
    plt.figure(figsize=(8, 5))
    for nome in tempo_verde.terms:
        mf = tempo_verde.terms[nome].mf
        plt.plot(x_tempo_verde, mf, label=nome.capitalize())
    plt.title('Funções de Pertinência do Tempo de Verde')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Pertinência')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/pertinencia.png')
    plt.close()
