import reflex as rx
import sys
import os
import json
import ast
import re
from datetime import datetime
from typing import List

# allow access to parent folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# backend imports
from ai_suggester import review_code
from error_detector import analyze_code
from Code_parser import parse_code


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.allocation_in_loop = False
        self.recursion = False
        self._current_func = None

    def visit_FunctionDef(self, node):
        prev = self._current_func
        self._current_func = node.name
        self.generic_visit(node)
        self._current_func = prev

    def visit_For(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Call(self, node):
        if self._current_func and isinstance(node.func, ast.Name):
            if node.func.id == self._current_func:
                self.recursion = True
        self.generic_visit(node)

    def _mark_allocation(self):
        if self.loop_depth > 0:
            self.allocation_in_loop = True

    def visit_ListComp(self, node):
        self._mark_allocation()
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self._mark_allocation()
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self._mark_allocation()
        self.generic_visit(node)

    def visit_List(self, node):
        self._mark_allocation()
        self.generic_visit(node)

    def visit_Dict(self, node):
        self._mark_allocation()
        self.generic_visit(node)

    def visit_Set(self, node):
        self._mark_allocation()
        self.generic_visit(node)


def estimate_complexity(code: str) -> tuple[str, str]:
    try:
        tree = ast.parse(code)
    except Exception:
        return "O(?)", "O(?)"

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    if visitor.max_loop_depth <= 0:
        time_complexity = "O(1)"
    elif visitor.max_loop_depth == 1:
        time_complexity = "O(n)"
    elif visitor.max_loop_depth == 2:
        time_complexity = "O(n^2)"
    elif visitor.max_loop_depth == 3:
        time_complexity = "O(n^3)"
    else:
        time_complexity = f"O(n^{visitor.max_loop_depth})"

    if visitor.recursion or visitor.allocation_in_loop:
        space_complexity = "O(n)"
    else:
        space_complexity = "O(1)"

    return time_complexity, space_complexity


def extract_ai_complexities(text: str) -> tuple[str, str]:
    if not text:
        return "", ""

    time_match = re.search(r"time\s*complexity\s*[:\-]?\s*(O\([^\n\r\)]+\))", text, re.IGNORECASE)
    space_match = re.search(r"space\s*complexity\s*[:\-]?\s*(O\([^\n\r\)]+\))", text, re.IGNORECASE)

    time_complexity = time_match.group(1) if time_match else ""
    space_complexity = space_match.group(1) if space_match else ""

    return time_complexity, space_complexity


class State(rx.State):
    code: str = ""
    language: str = "Python"
    loading: bool = False
    optimized_code: str = ""
    history: List[str] = []
    errors: list = []
    style: list = []
    optimizations: list = []
    summary: str = ""
    analysis_score: int = 0
    current_page: str = "home"
    time_complexity: str = "O(1)"
    space_complexity: str = "O(1)"

    # Enhanced history with more details
    analysis_history: List[dict] = []

    # Extracted corrected code for display
    corrected_code: str = ""

    def _history_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "analysis_history.json")

    def save_history(self):
        try:
            with open(self._history_path(), "w", encoding="utf-8") as handle:
                json.dump(self.analysis_history, handle, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_history(self):
        try:
            path = self._history_path()
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                if isinstance(data, list):
                    self.analysis_history = data
        except Exception:
            pass

    def set_code(self, value: str):
        self.code = value

    def extract_corrected_code(self, ai_response: str) -> str:
        """Extract just the corrected code from AI response"""
        if not ai_response:
            return "No corrected code available."

        lines = ai_response.split("\n")
        improved_code_start = -1

        for i, line in enumerate(lines):
            if "Improved Code:" in line:
                improved_code_start = i
                break

        if improved_code_start == -1:
            in_code_block = False
            code_lines = []

            for line in lines:
                if line.strip() == "```python":
                    in_code_block = True
                    continue
                if line.strip() == "```":
                    in_code_block = False
                    continue
                if in_code_block:
                    code_lines.append(line)

            if code_lines:
                return "\n".join(code_lines)
            return "No corrected code found in AI response."

        code_lines = []
        in_code_block = False

        for line in lines[improved_code_start + 1 :]:
            if line.strip() == "```python":
                in_code_block = True
                continue
            if line.strip() == "```":
                in_code_block = False
                continue
            if in_code_block:
                code_lines.append(line)

        if code_lines:
            return "\n".join(code_lines)

        return "No corrected code found in AI response."

    def analyze(self):
        if not self.code.strip():
            self.errors = ["Please enter some code to analyze"]
            self.summary = "No code provided"
            self.optimizations = []
            self.style = []
            self.analysis_score = 0
            self.corrected_code = "No corrected code available."
            self.time_complexity = "O(?)"
            self.space_complexity = "O(?)"
            return

        self.loading = True
        self.errors = []
        self.style = []
        self.optimizations = []
        self.corrected_code = ""

        try:
            error_result = analyze_code(self.code)
            if "error" in error_result:
                self.errors = [error_result["error"]]
                base_score = 0
            else:
                self.errors = error_result.get("unused", [])
                base_score = int(error_result.get("score", 100))

            self.style = parse_code(self.code)

            style_penalty = min(len(self.style) * 2, 20)
            error_penalty = min(len(self.errors) * 3, 30)
            self.analysis_score = max(base_score - style_penalty - error_penalty, 0)

            # Default complexity from heuristic; may be overridden by AI response
            heuristic_time, heuristic_space = estimate_complexity(self.code)
            self.time_complexity = heuristic_time
            self.space_complexity = heuristic_space

            try:
                ai_response = review_code(self.code)
                self.optimizations = ai_response.get("optimizations", [])
                if not self.optimizations:
                    self.optimizations = ["No specific suggestions available for this code."]

                full_ai_response = ai_response.get("raw_text", "")
                if full_ai_response:
                    self.corrected_code = self.extract_corrected_code(full_ai_response)
                    ai_time, ai_space = extract_ai_complexities(full_ai_response)
                elif self.optimizations:
                    combined = "\n".join(self.optimizations)
                    self.corrected_code = self.extract_corrected_code(combined)
                    ai_time, ai_space = extract_ai_complexities(combined)
                else:
                    self.corrected_code = "No corrected code found in AI response."
                    ai_time, ai_space = "", ""

                if ai_time:
                    self.time_complexity = ai_time
                if ai_space:
                    self.space_complexity = ai_space

                if not self.corrected_code:
                    self.corrected_code = "No corrected code found in AI response."

            except Exception as ai_error:
                self.optimizations = [f"AI analysis unavailable: {str(ai_error)}"]
                self.corrected_code = "AI analysis unavailable."

            self.summary = f"Code Quality Score: {self.analysis_score}/100"

            history_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": int(self.analysis_score),
                "issues_count": len(self.errors),
                "suggestions_count": len(self.optimizations),
                "style_count": len(self.style),
                "code_preview": self.code[:100] + "..." if len(self.code) > 100 else self.code,
                "full_code": self.code,
                "errors": self.errors.copy(),
                "optimizations": self.optimizations.copy(),
                "style": self.style.copy(),
                "corrected_code": self.corrected_code,
                "time_complexity": self.time_complexity,
                "space_complexity": self.space_complexity,
            }
            self.analysis_history = [history_entry] + self.analysis_history
            self.save_history()

        except Exception as e:
            self.errors = [f"Analysis failed: {str(e)}"]
            self.summary = "Analysis failed."
            self.optimizations = []
            self.style = []
            self.analysis_score = 0
            self.corrected_code = "Analysis failed."
            self.time_complexity = "O(?)"
            self.space_complexity = "O(?)"

        self.loading = False

        entry = f"Score: {self.analysis_score}/100 | {len(self.errors)} issues | {len(self.optimizations)} suggestions"
        self.history = self.history + [entry]

    def download_report(self):
        content = f"""AI Code Review Report

==========================================
CODE ANALYSIS
==========================================

Code:
{self.code}

==========================================
QUALITY SCORE
==========================================
{self.summary}

==========================================
ISSUES FOUND ({len(self.errors)})
==========================================
{chr(10).join([f"â€¢ {error}" for error in self.errors]) if self.errors else "No issues found."}

==========================================
STYLE ANALYSIS ({len(self.style)} items)
==========================================
{chr(10).join([f"â€¢ {style}" for style in self.style[:10]]) if self.style else "No style issues found."}
{f"... and {len(self.style) - 10} more items" if len(self.style) > 10 else ""}

==========================================
AI SUGGESTIONS ({len(self.optimizations)})
==========================================
{chr(10).join([f"â€¢ {opt}" for opt in self.optimizations]) if self.optimizations else "No suggestions available."}

==========================================
CORRECTED CODE
==========================================
{self.corrected_code}

==========================================
SUMMARY
==========================================
Analysis completed successfully.
Total issues: {len(self.errors)}
Total suggestions: {len(self.optimizations)}
Overall score: {self.analysis_score}/100
"""

        return rx.download(
            data=content,
            filename="code_review_report.txt",
        )

    def set_current_page(self, page: str):
        self.current_page = page

    def load_history_entry(self, entry: dict):
        """Load a historical analysis entry into current state"""
        self.code = entry.get("full_code", entry.get("code_preview", ""))
        self.errors = entry.get("errors", [])
        self.optimizations = entry.get("optimizations", [])
        self.style = entry.get("style", [])
        self.analysis_score = entry.get("score", 0)
        self.corrected_code = entry.get("corrected_code", "No corrected code available.")
        self.time_complexity = entry.get("time_complexity", "O(?)")
        self.space_complexity = entry.get("space_complexity", "O(?)")
        self.summary = f"Code Quality Score: {self.analysis_score}/100"
