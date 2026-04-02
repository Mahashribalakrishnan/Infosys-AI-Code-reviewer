import ast

class AIReview(ast.NodeVisitor):

    def __init__(self, code_lines):
        self.defined = set()
        self.used = set()
        self.score = 100
        self.code_lines = code_lines

    def visit_Import(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)

            if len(node.id) <= 1:
                self.score -= 2

        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        length = node.end_lineno - node.lineno

        if length > 25:
            self.score -= 5

        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            self.score -= 10
        elif isinstance(node.test, ast.Constant) and node.test.value == 1:
            self.score -= 10

        self.generic_visit(node)

    def report(self):
        unused = self.defined - self.used
        final_score = max(self.score - (3 * len(unused)), 0)

        return {
            "unused": list(unused),
            "score": final_score
        }


# ANALYSE CODE FUNCTION
def analyze_code(code):
    try:
        tree = ast.parse(code)
        reviewer = AIReview(code.split("\n"))
        reviewer.visit(tree)
        return reviewer.report()

    except SyntaxError as e:
        return {"error": f"Syntax Error: {e}"}