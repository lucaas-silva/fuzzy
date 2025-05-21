from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Utiliza backend não-interativo para gerar gráficos em servidor
import matplotlib.pyplot as plt
import numpy as np
import os
import random

# Inicializa a aplicação Flask
app = Flask(__name__)

# Função para gerar o gráfico da sequência de tempos de verde
def gerar_grafico_sequencia(tempos):
    """
    Gera um gráfico de linha com os tempos de verde calculados para cada segmento.
    Salva a imagem como 'static/plot.png'.
    """
    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(tempos)+1), tempos, marker='o', color='blue')
    plt.xlabel('Segmento')
    plt.ylabel('Tempo de Verde (s)')
    plt.title('Sequência de Tempos de Verde')
    plt.grid(True)
    plt.savefig(os.path.join('static', 'plot.png'))
    plt.close()

# Função para gerar o gráfico da previsão de fluxo futuro
def gerar_grafico_previsao(previsoes):
    """
    Gera um gráfico de linha com a previsão dos próximos ciclos de tempo de verde.
    Salva a imagem como 'static/previsao.png'.
    """
    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(previsoes)+1), previsoes, marker='o', color='orange')
    plt.xlabel('Ciclo Futuro')
    plt.ylabel('Tempo de Verde Previsto (s)')
    plt.title('Previsão de Fluxo Futuro')
    plt.grid(True)
    plt.savefig(os.path.join('static', 'previsao.png'))
    plt.close()

# Função para gerar o gráfico das funções de pertinência fuzzy
def gerar_grafico_pertinencia():
    """
    Gera o gráfico das funções de pertinência para Curto, Médio e Longo.
    Salva a imagem como 'static/pertinencia.png'.
    """
    x = np.linspace(0, 100, 100)  # Intervalo de tempos de 0 a 100
    # Funções de pertinência fuzzy
    curto = np.maximum(0, 1 - x / 30)
    medio = np.maximum(0, (x - 20) / 30) * np.maximum(0, (70 - x) / 30)
    longo = np.maximum(0, (x - 60) / 40)

    plt.figure(figsize=(6, 4))
    plt.plot(x, curto, label='Curto')
    plt.plot(x, medio, label='Médio')
    plt.plot(x, longo, label='Longo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Pertinência')
    plt.title('Funções de Pertinência')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join('static', 'pertinencia.png'))
    plt.close()

# Função para calcular o tempo de verde com base nas variáveis de entrada
def calcular_tempo(densidade, velocidade, espera, incidentes, emergencia=False):
    """
    Calcula o tempo de verde para um segmento utilizando uma fórmula ponderada.
    Aplica ajustes se o Modo Emergencial estiver ativado.
    
    Parâmetros:
        densidade (float): Quantidade de veículos.
        velocidade (float): Velocidade média.
        espera (float): Tempo de espera.
        incidentes (float): Número de incidentes.
        emergencia (bool): Se True, ativa o Modo Emergencial.
    
    Retorna:
        dict: {'tempo': tempo calculado, 'graus': pertinências, 'explicacao': texto explicativo}
    """
    # Fórmula de cálculo com pesos definidos
    tempo = densidade * 0.2 + espera * 0.3 - velocidade * 0.1 + incidentes * 5

    # Define o limite máximo dinamicamente
    limite_max = 120 if emergencia else 90

    if emergencia:
        tempo += 15  # Ajuste extra para emergência

    # Ajuste para manter o tempo dentro do intervalo permitido
    tempo = max(15, min(tempo, limite_max))

    # Cálculo das pertinências fuzzy
    curto = max(0, 1 - tempo / 30)
    medio = max(0, (tempo - 20) / 30) * max(0, (70 - tempo) / 30)
    longo = max(0, (tempo - 60) / 40)

    # Armazena os graus de pertinência arredondados
    graus = {'curto': round(curto, 2), 'medio': round(medio, 2), 'longo': round(longo, 2)}

    # Determina qual função é dominante
    dominante = max(graus, key=graus.get).upper()

    # Gera explicação automática
    explicacao = f"Função dominante: {dominante}."

    if emergencia:
        explicacao += " ⚠️ Modo Emergencial ativado: ajuste extra aplicado."

    return {
        'tempo': round(tempo, 2),
        'graus': graus,
        'explicacao': explicacao
    }

# Rota principal da aplicação
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal que trata requisições GET e POST.
    GET: exibe o formulário.
    POST: processa os dados de entrada, calcula os tempos, gera gráficos e renderiza o resultado.
    """
    resultados = None
    previsao = None

    if request.method == 'POST':
        resultados = []
        tempos = []

        # Verifica se o Modo Emergencial foi ativado
        emergencia = 'emergencia' in request.form

        # Processa os dados de entrada para cada segmento
        for i in range(1, 5):
            densidade = float(request.form[f'd{i}'])
            velocidade = float(request.form[f'v{i}'])
            espera = float(request.form[f'e{i}'])
            incidentes = float(request.form[f'inc{i}'])

            # Calcula o tempo de verde para o segmento
            resultado = calcular_tempo(densidade, velocidade, espera, incidentes, emergencia)
            resultados.append(resultado)
            tempos.append(resultado['tempo'])

        # Gera os gráficos baseados nos tempos calculados
        gerar_grafico_sequencia(tempos)
        gerar_grafico_pertinencia()

        # Previsão de fluxo futuro (3 ciclos)
        previsao = []
        ultimo = tempos[-1]

        for _ in range(3):
            # Variação aleatória de até ±5 segundos
            variacao = random.uniform(-5, 5)
            # Ajusta o tempo previsto para o intervalo permitido
            proximo = max(15, min(120, ultimo + variacao))
            previsao.append(round(proximo, 2))
            ultimo = proximo

        # Gera gráfico da previsão
        gerar_grafico_previsao(previsao)

    # Renderiza a página com os resultados e previsões
    return render_template('index.html', resultados=resultados, previsao=previsao)

# Executa a aplicação
if __name__ == '__main__':
    # Inicia o servidor Flask em modo debug
    app.run(debug=True)
