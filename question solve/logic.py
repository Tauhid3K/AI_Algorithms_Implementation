import itertools
import re


class LogicalEngine:
    """Parses propositional expressions, builds truth tables, and classifies them."""

    def preprocess_expression(self, expression: str) -> str:
        expr = expression

        # Handle OCR/unicode variants from exam sheets.
        expr = expr.replace("—i", "->").replace("—+", "->").replace("--4", "->").replace("--9", "->")
        expr = expr.replace(" IFE ", " IFF ")
        expr = expr.replace("<->", " IFF ")

        # Replace standalone A as AND in exam-style inputs like: (p -> q) A (q -> r)
        expr = re.sub(r"\bA\b", "AND", expr)

        # Convert implication repeatedly so nested parts are supported.
        while "->" in expr or "IMPLIES" in expr:
            new_expr = re.sub(
                r"(\w+|\([^()]+\))\s*(?:->|IMPLIES)\s*(\w+|\([^()]+\))",
                r"(not (\1) or (\2))",
                expr,
            )
            if new_expr == expr:
                break
            expr = new_expr

        # Convert remaining logical operators to Python boolean operators.
        expr = expr.replace("IFF", " == ")
        expr = re.sub(r"\bAND\b|\^|&", " and ", expr)
        expr = re.sub(r"\bOR\b|\bv\b|\|", " or ", expr)
        expr = re.sub(r"\bNOT\b|~", " not ", expr)
        return expr

    def get_variables(self, expression: str):
        words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", expression)
        keywords = {"and", "or", "not", "true", "false", "if", "else"}
        return sorted({w for w in words if w.lower() not in keywords})

    @staticmethod
    def classify(results):
        if all(results):
            return "Tautology (always true)"
        if not any(results):
            return "Contradiction (always false)"
        return "Contingent (mixed true/false)"

    def generate_truth_table(self, expression: str, description: str = ""):
        python_expr = self.preprocess_expression(expression)
        variables = self.get_variables(python_expr)
        assignments = list(itertools.product([True, False], repeat=len(variables)))

        print(f"\n[Task] {description or 'Logical Expression'}")
        print(f"Expression: {expression}")

        header = " | ".join(variables) + " | Result"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        results = []
        for combo in assignments:
            env = dict(zip(variables, combo))
            value = bool(eval(python_expr, {"__builtins__": None}, env))
            results.append(value)
            row = " | ".join("T" if env[v] else "F" for v in variables)
            print(f"{row} | {'T' if value else 'F'}")

        print("-" * len(header))
        print(f"Classification: {self.classify(results)}")


if __name__ == "__main__":
    engine = LogicalEngine()

    # Exam-style sample with non-standard symbols.
    engine.generate_truth_table(
        "(p —i q) A (q -> r) —+ (p --4 r)",
        "Parse, evaluate, truth table, classification",
    )
