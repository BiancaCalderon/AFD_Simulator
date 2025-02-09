import json
# Definir precedencias y operadores
precedence = {'*': 3, '.': 2, '|': 1}
operators = {'*', '.', '|'}
output = []
stack = []
# Función para agregar operadores de concatenación explícitos
def insert_concatenation_operators(regex):
    result = []
    for i in range(len(regex)):
        result.append(regex[i])
        if i + 1 < len(regex):
            if (regex[i] not in operators and regex[i] != '(' and regex[i + 1] not in operators and regex[i + 1] != ')'):
                result.append('.')
            if (regex[i] == '*' and regex[i + 1] not in operators and regex[i + 1] != ')'):
                result.append('.')
    return ''.join(result)
# Función para convertir una expresión regular a postfix (Shunting Yard)
def shunting_yard(regex):
    output.clear()
    stack.clear()
    for token in regex:
        if token not in operators and token != '(' and token != ')':
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[token] <= precedence[stack[-1]]:
                output.append(stack.pop())
            stack.append(token)
    
    while stack:
        output.append(stack.pop())
    
    return ''.join(output)
# Función para guardar el resultado en un archivo JSON
def save_postfix_to_json(postfix, filename):
    data = {
        "postfix": postfix
    }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
# Solicitar al usuario que ingrese una expresión regular
regex = input("Ingresa una expresión regular (usa '_' para ε): ")
# Insertar operadores de concatenación explícitos
regex = insert_concatenation_operators(regex)
# Convertir la expresión regular a postfix
postfix = shunting_yard(regex)
# Mostrar el resultado
print("Postfix:", postfix)
# Guardar el resultado en un archivo JSON
save_postfix_to_json(postfix, 'postfix_output.json')
print("El resultado ha sido guardado en 'postfix_output.json'")