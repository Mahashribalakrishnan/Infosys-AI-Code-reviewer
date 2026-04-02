import ast

def parse_code(code):
    result = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result.append(f"Import: {alias.name}")

            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    result.append(f"Variable created: {node.id}")
                elif isinstance(node.ctx, ast.Load):
                    result.append(f"Variable used: {node.id}")

        return result

    except SyntaxError as e:
        return [f"Syntax Error: {str(e)}"]