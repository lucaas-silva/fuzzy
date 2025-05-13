import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def get_rules(densidade, velocidade, espera, incidentes, tempo_verde):
    rules = [
        # Densidade Baixa
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['baixa'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['baixa'] & incidentes['media'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['baixa'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['media'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['media'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['baixa'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['baixa'] & incidentes['baixa'], tempo_verde['longo']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['baixa'] & incidentes['media'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['baixa'] & incidentes['alta'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['media'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['media'] & incidentes['media'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['media'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['baixa'] & incidentes['baixa'], tempo_verde['longo']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['baixa'] & incidentes['media'], tempo_verde['longo']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['baixa'] & incidentes['alta'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['media'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['media'] & incidentes['media'], tempo_verde['medio']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['baixa'] & velocidade['alta'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        # Densidade Média
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['baixa'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['baixa'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['baixa'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['media'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['media'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['baixa'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['baixa'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['baixa'] & incidentes['media'], tempo_verde['medio']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['baixa'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['media'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['media'] & incidentes['media'], tempo_verde['medio']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['media'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['baixa'] & incidentes['baixa'], tempo_verde['longo']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['baixa'] & incidentes['media'], tempo_verde['medio']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['baixa'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['media'] & incidentes['baixa'], tempo_verde['medio']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['media'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['media'] & velocidade['alta'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        # Densidade Alta
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['baixa'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['baixa'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['baixa'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['media'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['media'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['baixa'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['baixa'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['baixa'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['baixa'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['media'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['media'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['media'] & espera['alta'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['baixa'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['baixa'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['baixa'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['media'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['media'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['media'] & incidentes['alta'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['alta'] & incidentes['baixa'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['alta'] & incidentes['media'], tempo_verde['curto']),
        ctrl.Rule(densidade['alta'] & velocidade['alta'] & espera['alta'] & incidentes['alta'], tempo_verde['curto'])
    ]
    return rules


def define_universes():
    """Define os universos de discurso para as variáveis."""
    return {
        'densidade': np.arange(0, 201, 1),
        'velocidade': np.arange(0, 71, 1),
        'espera': np.arange(0, 151, 1),
        'incidentes': np.arange(0, 6.1, 0.1),
        'tempo_verde': np.arange(0, 91, 1)
    }


def create_antecedents(universes):
    """Cria os antecedentes (entradas) do sistema fuzzy."""
    return {
        'densidade': ctrl.Antecedent(universes['densidade'], 'densidade'),
        'velocidade': ctrl.Antecedent(universes['velocidade'], 'velocidade'),
        'espera': ctrl.Antecedent(universes['espera'], 'espera'),
        'incidentes': ctrl.Antecedent(universes['incidentes'], 'incidentes')
    }


def create_consequent(universe):
    """Cria o consequente (saída) do sistema fuzzy."""
    return ctrl.Consequent(universe, 'tempo_verde')


def define_membership_functions(antecedents, consequent, universes):
    """Define as funções de pertinência para antecedentes e consequente."""
    # Densidade
    antecedents['densidade']['baixa'] = fuzz.zmf(universes['densidade'], 0, 60)
    antecedents['densidade']['media'] = fuzz.trimf(universes['densidade'], [50, 85, 120])
    antecedents['densidade']['alta'] = fuzz.smf(universes['densidade'], 110, 200)

    # Velocidade
    antecedents['velocidade']['baixa'] = fuzz.zmf(universes['velocidade'], 0, 25)
    antecedents['velocidade']['media'] = fuzz.trimf(universes['velocidade'], [20, 35, 50])
    antecedents['velocidade']['alta'] = fuzz.smf(universes['velocidade'], 45, 70)

    # Espera
    antecedents['espera']['baixa'] = fuzz.zmf(universes['espera'], 0, 40)
    antecedents['espera']['media'] = fuzz.trimf(universes['espera'], [30, 60, 90])
    antecedents['espera']['alta'] = fuzz.smf(universes['espera'], 85, 150)

    # Incidentes
    antecedents['incidentes']['baixa'] = fuzz.zmf(universes['incidentes'], 0, 1.5)
    antecedents['incidentes']['media'] = fuzz.trimf(universes['incidentes'], [1, 2.25, 3.5])
    antecedents['incidentes']['alta'] = fuzz.smf(universes['incidentes'], 3, 6)

    # Tempo verde
    consequent['curto'] = fuzz.zmf(universes['tempo_verde'], 0, 20)
    consequent['medio'] = fuzz.trimf(universes['tempo_verde'], [15, 32.5, 50])
    consequent['longo'] = fuzz.smf(universes['tempo_verde'], 45, 90)


def create_control_system(rules):
    """Cria o sistema de controle fuzzy."""
    sistema = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(sistema)


def adjust_green_time(green_time, segment_index, inputs):
    """Ajusta o tempo de verde com base em segmentos adjacentes."""
    adjustment = 0
    if segment_index > 0:
        prev_density = inputs[segment_index - 1][0]
        if prev_density > 120:
            adjustment += 5
    if segment_index < len(inputs) - 1:
        next_density = inputs[segment_index + 1][0]
        if next_density > 120:
            adjustment -= 5
    return min(max(green_time + adjustment, 0), 90)


def calculate_memberships(green_time, universe):
    """Calcula as pertinências para o tempo de verde."""
    return {
        'green_time': {
            'range': universe.tolist(),
            'curto': fuzz.zmf(universe, 0, 20).tolist(),
            'medio': fuzz.trimf(universe, [15, 32.5, 50]).tolist(),
            'longo': fuzz.smf(universe, 45, 90).tolist(),
            'value': green_time
        }
    }


def compute_green_times(inputs):
    """
    Calcula os tempos de verde e os graus de pertinência para cada entrada e saída.
    Entrada: lista de [densidade, velocidade, espera, incidentes] para cada segmento.
    Saída: [tempos de verde, graus de pertinência].
    """
    green_times = []
    memberships = []

    # Inicialização
    universes = define_universes()
    antecedents = create_antecedents(universes)
    tempo_verde = create_consequent(universes['tempo_verde'])
    define_membership_functions(antecedents, tempo_verde, universes)

    rules = get_rules(
        antecedents['densidade'],
        antecedents['velocidade'],
        antecedents['espera'],
        antecedents['incidentes'],
        tempo_verde
    )
    simulacao = create_control_system(rules)
    # Processamento por segmento
    for i, segment in enumerate(inputs):
        simulacao.input['densidade'] = segment[0]
        simulacao.input['velocidade'] = segment[1]
        simulacao.input['espera'] = segment[2]
        simulacao.input['incidentes'] = segment[3]

        simulacao.compute()
        green_time = simulacao.output['tempo_verde']
        green_time = adjust_green_time(green_time, i, inputs)
        green_times.append(green_time)

        segment_memberships = calculate_memberships(green_time, universes['tempo_verde'])
        memberships.append(segment_memberships)

    return [green_times, memberships]
