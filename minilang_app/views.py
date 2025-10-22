from django.shortcuts import render
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'minilang_app/index.html')

def run_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            # Aquí va tu lógica del intérprete MiniLang
            return JsonResponse({'success': True, 'output': 'Resultado de prueba'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def execute_minilang(code):
    """
    Intérprete simple de MiniLang
    """
    variables = {}
    output_lines = []
    
    lines = code.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Manejar print
        if line.startswith('print(') and line.endswith(')'):
            expr = line[6:-1].strip()
            result = evaluate_expression(expr, variables)
            output_lines.append(str(result))
            
        # Manejar asignación de variables
        elif '=' in line:
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            expr = parts[1].strip()
            
            if not var_name.isidentifier():
                raise ValueError(f"Nombre de variable inválido: {var_name}")
                
            result = evaluate_expression(expr, variables)
            variables[var_name] = result
    
    return '\n'.join(output_lines)

def evaluate_expression(expr, variables):
    """
    Evalúa expresiones matemáticas simples
    """
    expr = expr.strip()
    
    # Si es un número
    if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
        return int(expr)
    
    # Si es una variable
    if expr in variables:
        return variables[expr]
    
    # Operaciones matemáticas
    operators = ['+', '-', '*', '/']
    for op in operators:
        if op in expr:
            parts = expr.split(op, 1)
            left = evaluate_expression(parts[0].strip(), variables)
            right = evaluate_expression(parts[1].strip(), variables)
            
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise ValueError("División por cero")
                return left // right  # División entera
    
    # Si no reconocemos la expresión
    raise ValueError(f"Expresión no válida: {expr}")
