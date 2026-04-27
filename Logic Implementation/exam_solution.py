import itertools
import re

class PropositionalLogicEngine:
    """
    Topic 1: Logic Implementation
    A core engine to parse, evaluate, and classify propositional logic expressions.
    """
    def preprocess_expression(self, expression):
        # Convert logic symbols to Python operators
        expr = expression
        
        # 1. Biconditional (IFF)
        expr = expr.replace('<->', ' == ').replace('IFF', ' == ')
        
        # 2. Implication (->)
        # We use a loop and regex to handle nested implications like (p -> q) -> r
        while '->' in expr or 'IMPLIES' in expr:
            # This regex identifies (Part A) -> (Part B)
            new_expr = re.sub(r'(\w+|\([^()]+\))\s*(?:->|IMPLIES)\s*(\w+|\([^()]+\))', r'(not (\1) or (\2))', expr)
            if new_expr == expr: break
            expr = new_expr
            
        # 3. Basic Operators
        # AND: ^, &, AND
        expr = re.sub(r'\bAND\b|\b\^\b|\b&\b', ' and ', expr)
        # OR: v, |, OR
        expr = re.sub(r'\bOR\b|\bv\b|\|', ' or ', expr)
        # NOT: ~, NOT
        expr = re.sub(r'\bNOT\b|~', ' not ', expr)
        
        return expr

    def get_variables(self, expression):
        # Find all unique words that aren't keywords
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression)
        keywords = {'and', 'or', 'not', 'true', 'false', 'iff', 'implies', 'v', 'if', 'else'}
        return sorted(list(set(w for w in words if w.lower() not in keywords)))

    def solve(self, expression, description=""):
        variables = self.get_variables(expression)
        combinations = list(itertools.product([True, False], repeat=len(variables)))
        
        print(f"\n{'='*60}")
        print(f"TASK: {description}")
        print(f"EXPRESSION: {expression}")
        print(f"{'='*60}")
        
        # Print Header
        header = " | ".join(variables) + " | Result"
        print(header)
        print("-" * len(header))
        
        results = []
        python_logic = self.preprocess_expression(expression)
        
        for combo in combinations:
            assignments = dict(zip(variables, combo))
            # Evaluate using Python's engine
            res = eval(python_logic, {"__builtins__": None}, assignments)
            results.append(res)
            
            # Print Row
            row = " | ".join("T" if assignments[v] else "F" for v in variables)
            print(f"{row} | {'T' if res else 'F'}")
        
        # Classification
        print("-" * len(header))
        if all(results): 
            print("CLASSIFICATION: Tautology (Always True)")
        elif not any(results): 
            print("CLASSIFICATION: Contradiction (Always False)")
        else: 
            print("CLASSIFICATION: Contingent (True in some cases, False in others)")

if __name__ == "__main__":
    engine = PropositionalLogicEngine()

    # 1. Complex Example: Law of Syllogism
    # Interpreting: (p -> q) AND (q -> r) -> (p -> r)
    syllogism = "(p -> q) AND (q -> r) -> (p -> r)"
    engine.solve(syllogism, "Input Example: Law of Syllogism")

    # 2. Natural Language Propositions (a-e)
    tasks = [
        ("p <-> q", "a. Raining iff Cloudy Day"),
        ("p -> q", "b. Score 100 implies earning an A"),
        ("p OR q", "c. Take 2 Advil or 3 Tylenol"),
        ("p OR q", "d. Studied hard or extremely bright"),
        ("p AND q", "e. I am a rock and I am an island")
    ]

    for expr, desc in tasks:
        engine.solve(expr, desc)
