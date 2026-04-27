import itertools
import re

class PropositionalLogicEngine:
    """
    Topic 1: Logic Implementation
    A core engine to parse, evaluate, and classify propositional logic expressions.
    """
    def preprocess_expression(self, expression):
        expr = expression
        # Handle exam-specific symbols from the input example
        expr = expr.replace('—i', '->').replace('—+', '->').replace('--9', '->')
        expr = expr.replace(' A ', ' AND ')
        
        expr = expr.replace('<->', ' == ').replace('IFF', ' == ')
        while '->' in expr or 'IMPLIES' in expr:
            new_expr = re.sub(r'(\w+|\([^()]+\))\s*(?:->|IMPLIES)\s*(\w+|\([^()]+\))', r'(not (\1) or (\2))', expr)
            if new_expr == expr: break
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
        # Preprocess first to convert symbols like —i to ->
        python_logic = self.preprocess_expression(expression)
        
        # Now get variables from the cleaned expression
        variables = self.get_variables(python_logic)
        combinations = list(itertools.product([True, False], repeat=len(variables)))
        
        print(f"\n[Task] {description}")
        print(f"Logic: {expression}")
        
        header = " | ".join(variables) + " | Result"
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        
        results = []
        for combo in combinations:
            assignments = dict(zip(variables, combo))
            res = eval(python_logic, {"__builtins__": None}, assignments)
            results.append(res)
            print(" | ".join("T" if assignments[v] else "F" for v in variables) + f" | {'T' if res else 'F'}")
        
        print("-" * len(header))
        # Exact classification strings from your requirements
        if all(results): 
            print("Classification: A Tautology (always true)")
        elif not any(results): 
            print("Classification: A Contradiction (always false)")
        else: 
            print("Classification: Contingent (true for some assignments and false for others)")

if __name__ == "__main__":
    engine = PropositionalLogicEngine()
    
    print("=== LOGIC ENGINE DEMO ===")

    # 1. The Exam's Complex Example
    # Using the exact symbols from your question (—i, A, —+, --9)
    engine.generate_truth_table("(p —i q) A (q —i r) —+ (p --9 r)", "Exam Syllogism Example")

    # 2. Natural Language Propositions (a-e)
    tasks = [
        ("p <-> q", "a. Raining iff Cloudy Day"),
        ("p -> q", "b. Score 100 implies earning an A"),
        ("p OR q", "c. Take 2 Advil or 3 Tylenol"),
        ("p OR q", "d. Studied hard or extremely bright"),
        ("p AND q", "e. I am a rock and I am an island")
    ]

    for expr, desc in tasks:
        engine.generate_truth_table(expr, desc)

    # 3. Specific Classification Demos
    engine.generate_truth_table("p OR NOT p", "Demo: Known Tautology")
    engine.generate_truth_table("p AND NOT p", "Demo: Known Contradiction")
