import ast
lines = []
while True:
    line = input()
    if line.strip() == "end":
        break
    lines.append(line)

code = "\n".join(lines)

try:
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                print(f" Import Node: Library name '{alias.name}'")
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                print(f" Variable Node (Creation): Variable name '{node.id}'")
            elif isinstance(node.ctx, ast.Load):
                print(f" Variable Node (Usage): '{node.id}' is being used")
except SyntaxError as e:
    print(f"Syntax Error: {str(e)}")