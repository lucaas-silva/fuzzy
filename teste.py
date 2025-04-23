


import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Universos
x_densidade = np.arange(0, 201, 1)
x_velocidade = np.arange(0, 71, 1)
x_espera = np.arange(0, 151, 1)
x_incidentes = np.arange(0, 6.1, 0.1)

# Densidade (com intersecção acima de 0.5)
densidade_baixa = fuzz.zmf(x_densidade, 80, 110)
densidade_media = fuzz.trapmf(x_densidade, [90, 100, 120, 130])
densidade_alta = fuzz.smf(x_densidade, 110, 140)

# Velocidade
velocidade_baixa = fuzz.zmf(x_velocidade, 25, 40)
velocidade_media = fuzz.trapmf(x_velocidade, [30, 35, 45, 55])
velocidade_alta = fuzz.smf(x_velocidade, 45, 55)

# Tempo de Espera
espera_baixa = fuzz.zmf(x_espera, 30, 60)
espera_media = fuzz.trapmf(x_espera, [40, 50, 70, 95])
espera_alta = fuzz.smf(x_espera, 75, 95)

# Incidentes
incidentes_baixo = fuzz.zmf(x_incidentes, 2, 3)
incidentes_medio = fuzz.trapmf(x_incidentes, [2, 3, 3.5, 4.5])
incidentes_alto = fuzz.smf(x_incidentes, 3.5, 4.7)

# Plotagem
fig, axs = plt.subplots(2, 2, figsize=(16, 10))

# Densidade
axs[0, 0].plot(x_densidade, densidade_baixa, label='Baixa')
axs[0, 0].plot(x_densidade, densidade_media, label='Média')
axs[0, 0].plot(x_densidade, densidade_alta, label='Alta')
axs[0, 0].set_title('Densidade de Veículos')
axs[0, 0].legend()

# Velocidade
axs[0, 1].plot(x_velocidade, velocidade_baixa, label='Baixa')
axs[0, 1].plot(x_velocidade, velocidade_media, label='Média')
axs[0, 1].plot(x_velocidade, velocidade_alta, label='Alta')
axs[0, 1].set_title('Velocidade Média (km/h)')
axs[0, 1].legend()

# Espera
axs[1, 0].plot(x_espera, espera_baixa, label='Baixa')
axs[1, 0].plot(x_espera, espera_media, label='Média')
axs[1, 0].plot(x_espera, espera_alta, label='Alta')
axs[1, 0].set_title('Tempo de Espera (s)')
axs[1, 0].legend()

# Incidentes
axs[1, 1].plot(x_incidentes, incidentes_baixo, label='Baixo')
axs[1, 1].plot(x_incidentes, incidentes_medio, label='Médio')
axs[1, 1].plot(x_incidentes, incidentes_alto, label='Alto')
axs[1, 1].set_title('Número de Incidentes')
axs[1, 1].legend()

plt.tight_layout()
plt.show()
