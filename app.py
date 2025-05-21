from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# Importações do sistema fuzzy
from fuzzy_logic import (
    calcular_tempo_fuzzy,
    calcular_graus_pertinencia,
    gerar_explicacao,
    plotar_funcoes_pertinencia
)

app = Flask(__name__)

# Gera gráfico da sequência de tempos
def gerar_grafico_sequencia(tempos):
    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(tempos)+1), tempos, marker='o', color='blue')
    plt.xlabel('Segmento')
    plt.ylabel('Tempo de Verde (s)')
    plt.title('Sequência de Tempos de Verde')
    plt.grid(True)
    plt.savefig(os.path.join('static', 'plot.png'))
    plt.close()

# Gera gráfico da previsão de fluxo futuro
def gerar_grafico_previsao(previsoes):
    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(previsoes)+1), previsoes, marker='o', color='orange')
    plt.xlabel('Ciclo Futuro')
    plt.ylabel('Tempo de Verde Previsto (s)')
    plt.title('Previsão de Fluxo Futuro')
    plt.grid(True)
    plt.savefig(os.path.join('static', 'previsao.png'))
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = None
    previsao = None

    if request.method == 'POST':
        resultados = []
        tempos = []

        emergencia = 'emergencia' in request.form  # Detecta Modo Emergencial

        for i in range(1, 5):
            d = float(request.form[f'd{i}'])
            v = float(request.form[f'v{i}'])
            e = float(request.form[f'e{i}'])
            inc = float(request.form[f'inc{i}'])

            # Cálculo via sistema fuzzy
            tempo = calcular_tempo_fuzzy(d, v, e, inc)

            # Ajuste do tempo para o Modo Emergencial
            if emergencia:
                tempo = min(120, tempo + 15)  # Limite de 120s

            # Cálculo de pertinências e explicação
            graus = calcular_graus_pertinencia(tempo)
            explicacao = gerar_explicacao(graus)

            if emergencia:
                explicacao += " ⚠️ Modo Emergencial ativado: ajuste extra aplicado."

            # Organiza resultado
            resultado = {
                'tempo': round(tempo, 2),
                'graus': {k: round(v, 2) for k, v in graus.items()},
                'explicacao': explicacao
            }

            resultados.append(resultado)
            tempos.append(resultado['tempo'])

        # Geração dos gráficos
        gerar_grafico_sequencia(tempos)
        plotar_funcoes_pertinencia()

        # Previsão de fluxo futuro
        previsao = []
        ultimo = tempos[-1]

        for _ in range(3):
            variacao = random.uniform(-5, 5)
            proximo = max(15, min(120, ultimo + variacao))
            previsao.append(round(proximo, 2))
            ultimo = proximo

        gerar_grafico_previsao(previsao)

    return render_template('index.html', resultados=resultados, previsao=previsao)

if __name__ == '__main__':
    app.run(debug=True)
