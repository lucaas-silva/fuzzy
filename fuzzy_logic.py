import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definição dos universos de discurso (domínios das variáveis)
x_densidade = np.arange(0, 201, 1)
x_velocidade = np.arange(0, 71, 1)
x_espera = np.arange(0, 151, 1)
x_incidentes = np.arange(0, 6.1, 0.1)
x_tempo_verde = np.arange(0, 91, 1)

# Definição das variáveis fuzzy de entrada (antecedentes)
densidade = ctrl.Antecedent(x_densidade, 'densidade')
velocidade = ctrl.Antecedent(x_velocidade, 'velocidade')
espera = ctrl.Antecedent(x_espera, 'espera')
incidentes = ctrl.Antecedent(x_incidentes, 'incidentes')

# Definição da variável fuzzy de saída (consequente)
tempo_verde = ctrl.Consequent(x_tempo_verde, 'tempo_verde')

# Definição das funções de pertinência para a saída
tempo_verde['curto'] = fuzz.trimf(x_tempo_verde, [0, 15, 30])
tempo_verde['medio'] = fuzz.trimf(x_tempo_verde, [20, 35, 50])
tempo_verde['longo'] = fuzz.trimf(x_tempo_verde, [40, 65, 90])

# Definição das funções de pertinência para as entradas
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

# Definição das regras fuzzy com base em pontuação de prioridade
rules = []
for d in ['baixa', 'media', 'alta']:
    for v in ['baixa', 'media', 'alta']:
        for e in ['baixa', 'media', 'alta']:
            for i in ['baixa', 'media', 'alta']:
                pontos = 0
                # Atribuição de pontos conforme intensidade de cada variável
                if d == 'alta': pontos += 2
                elif d == 'media': pontos += 1
                if v == 'baixa': pontos += 2
                elif v == 'media': pontos += 1
                if e == 'alta': pontos += 2
                elif e == 'media': pontos += 1
                if i == 'alta': pontos += 2
                elif i == 'media': pontos += 1

                # Determinação da saída com base na soma de pontos
                if pontos >= 7:
                    saida = 'longo'
                elif pontos >= 4:
                    saida = 'medio'
                else:
                    saida = 'curto'

                # Criação da regra fuzzy
                rule = ctrl.Rule(
                    densidade[d] & velocidade[v] & espera[e] & incidentes[i],
                    tempo_verde[saida]
                )
                rules.append(rule)

# Sistema de controle fuzzy
sistema_controle = ctrl.ControlSystem(rules)
sistema_simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Função para calcular o tempo de verde de forma sequencial
def calcular_tempo_verde_sequencial(segmentos):
    """
    Calcula os tempos de verde sequenciais para uma lista de segmentos,
    ajustando a densidade e a espera conforme o tempo anterior.

    Parâmetro:
        segmentos: lista de tuplas (densidade, velocidade, espera, incidentes)

    Retorno:
        Lista de tempos de verde calculados.
    """
    tempos = []
    ajuste = 0  # Ajuste inicial

    for idx, (d, v, e, i) in enumerate(segmentos):
        # Ajuste baseado no tempo anterior
        if ajuste > 0:
            d = max(0, d - ajuste)
            e = max(0, e - ajuste)
        elif ajuste < 0:
            d = min(200, d - ajuste)
            e = min(150, e - ajuste)
        
        # Definindo entradas
        sistema_simulacao.input['densidade'] = d
        sistema_simulacao.input['velocidade'] = v
        sistema_simulacao.input['espera'] = e
        sistema_simulacao.input['incidentes'] = i

        # Computa o sistema fuzzy
        sistema_simulacao.compute()

        # Obtém o tempo de verde calculado
        tempo = sistema_simulacao.output['tempo_verde']
        tempos.append(tempo)

        # Ajuste para o próximo segmento
        ajuste = tempo - 35  # Referência central em 35s

    return tempos

# Função para plotar o gráfico da sequência de tempos
def plotar_tempos(tempos):
    """
    Gera um gráfico mostrando a sequência dos tempos de verde.

    Parâmetro:
        tempos: lista de tempos de verde calculados.
    
    Saída:
        Gráfico salvo como 'static/plot.png'.
    """
    segmentos = list(range(1, len(tempos)+1))
    plt.figure(figsize=(8, 5))
    plt.plot(segmentos, tempos, marker='o', linestyle='-', color='b')
    
    # Adiciona o valor numérico sobre cada ponto
    for i, tempo in enumerate(tempos):
        plt.text(segmentos[i], tempo + 1, f"{tempo:.1f}", ha='center')
    
    plt.title('Sequência de Tempos de Verde por Segmento')
    plt.xlabel('Segmento')
    plt.ylabel('Tempo de Verde (s)')
    plt.ylim(0, max(tempos) + 10)
    plt.grid(True)
    plt.savefig('static/plot.png')
    plt.close()

# Função para plotar as funções de pertinência do tempo de verde
def plotar_funcoes_pertinencia():
    """
    Gera um gráfico das funções de pertinência do tempo de verde
    (Curto, Médio, Longo) e salva como 'static/pertinencia.png'.
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

# Função para calcular os graus de pertinência de um tempo específico
def calcular_graus_pertinencia(tempo):
    """
    Calcula os graus de pertinência do tempo informado
    para cada categoria: curto, médio e longo.

    Parâmetro:
        tempo: valor do tempo de verde.

    Retorno:
        Dicionário com o grau de pertinência para cada categoria.
    """
    graus = {}
    for nome in tempo_verde.terms:
        mf = tempo_verde.terms[nome].mf
        grau = fuzz.interp_membership(x_tempo_verde, mf, tempo)
        graus[nome] = grau
    return graus

# Função para gerar uma explicação baseada nos graus de pertinência
def gerar_explicacao(graus):
    """
    Gera uma explicação textual indicando qual categoria foi dominante.

    Parâmetro:
        graus: dicionário com graus de pertinência.

    Retorno:
        String com explicação sobre a função dominante.
    """
    dominante = max(graus, key=graus.get)
    explicacao = f"Função dominante: {dominante.upper()} → resultado influenciado por maior pertinência nesta categoria."
    return explicacao
