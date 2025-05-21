Controle Fuzzy de Semáforos 🚦
Este projeto implementa um sistema de controle inteligente de semáforos utilizando Lógica Fuzzy. O objetivo é calcular automaticamente o tempo de verde ideal para cada segmento de tráfego, considerando múltiplos fatores como densidade de veículos, velocidade, tempo de espera e número de incidentes.

O sistema inclui também um Modo Emergencial, que permite ajustar o tempo de verde para situações críticas, e uma Previsão de Fluxo Futuro, que simula os próximos ciclos de tempo de verde.

Funcionalidades
Cálculo do tempo de verde baseado nas variáveis de trânsito: densidade, velocidade, espera e incidentes.

Sistema de pertinência fuzzy com as categorias: Curto, Médio e Longo.

Identificação automática da Função Dominante com justificativa.

Modo Emergencial: aumenta o tempo de verde e permite ultrapassar o limite padrão de 90s, chegando até 120s.

Previsão de Fluxo Futuro: simula os próximos 3 ciclos.

Geração automática de gráficos:

Gráfico da sequência de tempos.

Gráfico das funções de pertinência.

Gráfico da previsão de fluxo futuro.

Interface web com tema Claro/Escuro e botão de Limpar Dados.

Tecnologias
Python

Flask (servidor web)

Matplotlib (geração de gráficos)

Numpy (operações matemáticas)

Instalação

Instale as dependências:

nginx
Copiar
Editar
pip install -r requirements.txt
Como Executar
nginx
Copiar
Editar
python app.py
Acesse no navegador: http://127.0.0.1:5000

Como Utilizar
Preencha os dados de entrada para cada Segmento:

Densidade (0 - 200)

Velocidade (0 - 70)

Espera (0 - 150)

Incidentes (0 - 6)

(Opcional) Marque "Ativar Modo Emergencial" para priorizar segurança.

Clique em "Calcular".

Visualize:

Tempos de verde calculados.

Graus de pertinência.

Gráficos: sequência, pertinência e previsão.

Explicação Técnica
Função calcular_tempo

Calcula o tempo de verde a partir dos dados inseridos, com pesos definidos por fator de influência:

Densidade → peso moderado.

Espera → peso forte.

Velocidade → impacto negativo.

Incidentes → impacto muito forte.

Ajusta o tempo com base no Modo Emergencial: se ativado, adiciona 15 segundos e permite limite máximo até 120 segundos.

Determina as pertinências (Curto, Médio, Longo) e a Função Dominante.

Previsão de Fluxo Futuro

Após calcular os tempos, simula os próximos 3 ciclos com variação aleatória de ±5 segundos.

Mostra ao usuário a tendência futura do fluxo.

Modo Emergencial

Quando ativado, aumenta o tempo de verde e amplia o limite máximo de segurança.

Justifica automaticamente a decisão na interface.

Geração de Gráficos

plot.png: gráfico da sequência de tempos.

pertinencia.png: gráfico das funções de pertinência.

previsao.png: gráfico da previsão futura.

Exemplo de Dados de Entrada
Segmento 1: Densidade=100, Velocidade=30, Espera=60, Incidentes=1
Segmento 2: Densidade=120, Velocidade=25, Espera=80, Incidentes=2
Segmento 3: Densidade=90, Velocidade=40, Espera=50, Incidentes=0.5
Segmento 4: Densidade=70, Velocidade=45, Espera=30, Incidentes=0

Possíveis Melhorias Futuras
Ajustar pesos automaticamente com algoritmos de Machine Learning.

Tornar a previsão mais precisa com base em dados históricos.

Implementar controle adaptativo em tempo real.

Melhorar a interface com mapas interativos.

Licença
Projeto desenvolvido para fins educacionais.