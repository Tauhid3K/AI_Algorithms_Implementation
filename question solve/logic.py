import itertools
import re


class PropositionalLogicEngine:
    """
    Topic 1: Logic Implementation
    A core engine to parse, evaluate, and classify propositional logic expressions.
    """

    def preprocess_expression(self, expression):
        expr = expression
        expr = expr.replace('<->', ' == ').replace('IFF', ' == ')
        while '->' in expr or 'IMPLIES' in expr:
            new_expr = re.sub(r'(\w+|\([^()]+\))\s*(?:->|IMPLIES)\s*(\w+|\([^()]+\))', r'(not (\1) or (\2))', expr)
            if new_expr == expr:
                break
            expr = new_expr
        expr = re.sub(r'\bAND\b|\b\^\b|\b&\b', ' and ', expr)
        expr = re.sub(r'\bOR\b|\bv\b|\|', ' or ', expr)
        expr = re.sub(r'\bNOT\b|~', ' not ', expr)
        return expr

    def get_variables(self, expression):
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression)
        keywords = {'and', 'or', 'not', 'true', 'false', 'iff', 'implies', 'v', 'if', 'else'}
        return sorted(list(set(w for w in words if w.lower() not in keywords)))

    def generate_truth_table(self, expression, description=""):
        variables = self.get_variables(expression)
        combinations = list(itertools.product([True, False], repeat=len(variables)))
        print(f"\n[Task] {description}\nLogic: {expression}")
        header = " | ".join(variables) + " | Result"
        print("-" * len(header) + "\n" + header + "\n" + "-" * len(header))

        results = []
        for combo in combinations:
            assignments = dict(zip(variables, combo))
            res = eval(self.preprocess_expression(expression), {"__builtins__": None}, assignments)
            results.append(res)
            print(" | ".join("T" if assignments[v] else "F" for v in variables) + f" | {'T' if res else 'F'}")

        if all(results):
            print("Classification: Tautology")
        elif not any(results):
            print("Classification: Contradiction")
        else:
            print("Classification: Contingent")


if __name__ == "__main__":
    engine = PropositionalLogicEngine()
    engine.generate_truth_table("(p -> q) AND (q -> r) -> (p -> r)", "Logic Engine Demo")
