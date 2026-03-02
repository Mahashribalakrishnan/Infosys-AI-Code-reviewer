import ast

class AIReview(ast.NodeVisitor):

    def __init__(self, code_lines):
        self.defined = set()
        self.used = set()
        self.score = 100
        self.code_lines = code_lines
        self.loop_depth = 0

    # IMPORT TRACKING

    def visit_Import(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    # VARIABLE TRACKING
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)

            # Poor variable name detection
            if len(node.id) <= 1:
                print(f"Poor variable name: '{node.id}'")
                self.score -= 2

        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

        self.generic_visit(node)

    # FUNCTION LENGTH CHECK

    def visit_FunctionDef(self, node):
        length = node.end_lineno - node.lineno

        if length > 25:
            print(f"Function '{node.name}' is too long ({length} lines)")
            self.score -= 5

        self.generic_visit(node)

    # INFINITE LOOP CHECK
   
    def visit_While(self, node):

        # Detect: while True
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            print("Infinite loop detected: 'while True'")
            self.score -= 10

        # Detect: while 1
        elif isinstance(node.test, ast.Constant) and node.test.value == 1:
            print("Infinite loop detected: 'while 1'")
            self.score -= 10

        self.generic_visit(node)

    # REPORT GENERATION

    def report(self):
        unused = self.defined - self.used

        print("\n--- AI Code Review Report ---")

        if unused:
            for item in unused:
                print(f"Unused variable/import: {item}")
                self.score -= 3
        else:
            print("No unused variables!")

        # Score grading
        final_score = max(self.score, 0)
        print(f"\nFinal Code Quality Score: {final_score}/100")

# TAKE USER INPUT

print("Enter your Python code (type END on a new line to finish):")

lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

code = "\n".join(lines)

# SYNTAX CHECK + REVIEW


try:
    tree = ast.parse(code)
    reviewer = AIReview(code.split("\n"))
    reviewer.visit(tree)
    reviewer.report()

except SyntaxError as e:
    print("\nSyntax Error Detected!")
    print(f"Message: {e.msg}")
    print(f"Line: {e.lineno}")
    print(f"Error Line: {e.text}")
    if e.offset:
        print(" " * (e.offset - 1) + "^")