import json
# Función para minimizar el AFD
def minimize_dfa(dfa):
    # Inicializar particiones
    partitions = [
        set(dfa["accept"]), 
        set(dfa["states"]) - set(dfa["accept"])
    ]
    
    # Refinar particiones
    def refine_partitions(partitions, dfa):
        alphabet = dfa["alphabet"]
        transition_map = {}
        
        for part in partitions:
            for state in part:
                transition_map[state] = {symbol: dfa["transitions"].get(state, {}).get(symbol) for symbol in alphabet}
        
        new_partitions = []
        for part in partitions:
            temp_part = {}
            for state in part:
                key = tuple(transition_map[state].values())
                if key not in temp_part:
                    temp_part[key] = set()
                temp_part[key].add(state)
            
            new_partitions.extend(temp_part.values())
            print("Minimizando AFD")
        return new_partitions
    
    # Refinar hasta que las particiones no cambien
    while True:
        new_partitions = refine_partitions(partitions, dfa)
        if len(new_partitions) == len(partitions):
            break
        partitions = new_partitions
    # Crear un mapeo de estados
    state_mapping = {}
    minimized_states = []
    new_state_count = 0
    
    for part in partitions:
        new_state = f"q{new_state_count}"
        for state in part:
            state_mapping[state] = new_state
        minimized_states.append(new_state)
        new_state_count += 1
    
    # Crear las nuevas transiciones
    minimized_transitions = {}
    for state, transitions in dfa["transitions"].items():
        minimized_state = state_mapping[state]
        if minimized_state not in minimized_transitions:
            minimized_transitions[minimized_state] = {}
        for symbol, target_state in transitions.items():
            minimized_transitions[minimized_state][symbol] = state_mapping[target_state]
    
    # Definir el estado inicial y los estados de aceptación
    minimized_start = state_mapping[dfa["start"]]
    minimized_accept = list(set(state_mapping[state] for state in dfa["accept"]))
    # Devolver el DFA minimizado
    minimized_dfa = {
        "states": minimized_states,
        "alphabet": dfa["alphabet"],
        "transitions": minimized_transitions,
        "start": minimized_start,
        "accept": minimized_accept
    }
    
    return minimized_dfa
# Función para guardar el AFD minimizado en formato JSON
def save_minimized_dfa_to_json(dfa, filename):
    with open(filename, 'w') as file:
        json.dump(dfa, file, indent=4)