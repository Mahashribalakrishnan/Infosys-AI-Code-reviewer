import ast
code = """
import math
side = 10
area = side*side
"""

tree = ast.parse(code)
print(ast.dump(tree, indent=2))
print(ast.unparse(tree))

for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            print(f" Import Node: Library name '{alias.name}'")

    if isinstance(node, ast.Name):
        if isinstance(node.ctx, ast.Store):
            print(f" Variable Node (Creation): Variable name '{node.id}'")
        elif isinstance(node.ctx, ast.Load):
            print(f" Variable Node (Usage): '{node.id}' is being used")