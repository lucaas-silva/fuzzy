Este projeto implementa um sistema de controle inteligente de semáforos utilizando Lógica Fuzzy. O objetivo é determinar automaticamente o tempo de verde mais adequado para cada segmento de tráfego, considerando fatores como:

Densidade de veículos.

Velocidade média.

Tempo de espera.

Número de incidentes.

O sistema possui ainda a funcionalidade opcional de Modo Emergencial, que ajusta automaticamente o tempo de verde para situações críticas.

✅ Funcionalidades Principais
Cálculo automático do tempo de verde com base em múltiplos fatores.

Sistema Fuzzy real com variáveis de entrada e saída, funções de pertinência e regras de inferência.

Determinação dos graus de pertinência e identificação da função dominante (Curto, Médio ou Longo).

Modo Emergencial: ao ser ativado pelo usuário, adiciona um ajuste extra de tempo, com limite de segurança.

Previsão de Fluxo Futuro: simula a tendência do tempo de verde para os próximos três ciclos.

Geração automática de gráficos:

Sequência de tempos de verde.

Funções de pertinência fuzzy.

Previsão de fluxo futuro.

Interface Web simples e funcional utilizando Flask.

Suporte para alternância entre modo normal e modo emergencial via checkbox no formulário.

✅ Como Funciona
O usuário preenche os valores para 4 segmentos de tráfego: densidade, velocidade, espera e incidentes.

O sistema processa cada segmento utilizando o sistema de inferência fuzzy:

Calcula o tempo de verde.

Determina os graus de pertinência para cada categoria.

Gera uma explicação automática com base na função dominante.

Se o Modo Emergencial for ativado, adiciona-se um ajuste extra de +15 segundos, respeitando o limite máximo de 120 segundos.

O sistema também calcula uma previsão de fluxo futuro com pequenas variações.

Todos os gráficos são gerados automaticamente e exibidos na interface.

✅ Tecnologias Utilizadas
Python 3

Flask — para criação da aplicação web.

scikit-fuzzy — para modelagem da lógica fuzzy.

Matplotlib — para geração de gráficos.

NumPy — para operações matemáticas.

 Como Utilizar
Preencha os valores de entrada para cada um dos 4 segmentos:

Densidade: 0 a 200

Velocidade: 0 a 70

Espera: 0 a 150

Incidentes: 0 a 6

(Opcional) Marque a opção "Ativar Modo Emergencial" para ajustar automaticamente o tempo de verde em situações críticas.

Clique no botão "Calcular".

Visualize:

Tempos de verde calculados.

Graus de pertinência para cada segmento.

Função dominante.

Gráficos gerados automaticamente.

Veja também a previsão de fluxo futuro.

✅ Exemplo de Entrada
Segmento 1: Densidade: 100, Velocidade: 30, Espera: 60, Incidentes: 1
Segmento 2: Densidade: 150, Velocidade: 20, Espera: 90, Incidentes: 2
Segmento 3: Densidade: 50, Velocidade: 50, Espera: 30, Incidentes: 0
Segmento 4: Densidade: 120, Velocidade: 25, Espera: 80, Incidentes: 1

✅ Explicação Técnica
A modelagem fuzzy define variáveis de entrada e saída com funções de pertinência Triangulares.

São geradas 81 regras que combinam as intensidades de todas as variáveis.

O sistema utiliza o scikit-fuzzy para realizar a inferência e a defuzzificação.

O Modo Emergencial adiciona um ajuste extra de tempo, com segurança limitada a 120 segundos.

O cálculo de previsão gera 3 valores futuros baseados no último tempo calculado, com variações aleatórias de até ±5 segundos.

Todos os gráficos são gerados com Matplotlib e exibidos na interface.

✅ Licença
Este projeto foi desenvolvido para fins educacionais e demonstrativos, ilustrando a aplicação de Lógica Fuzzy em sistemas de controle de tráfego.
