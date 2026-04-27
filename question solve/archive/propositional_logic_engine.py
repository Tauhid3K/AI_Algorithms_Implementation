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
        # IFF (P <-> Q) is True if both are same value
        expr = expr.replace('<->', ' == ').replace('IFF', ' == ')
        
        # Convert Implication (P -> Q) to (not P or Q)
        while '->' in expr or 'IMPLIES' in expr:
            new_expr = re.sub(r'(\w+|\([^()]+\))\s*(?:->|IMPLIES)\s*(\w+|\([^()]+\))', r'(not (\1) or (\2))', expr)
            if new_expr == expr: break
            expr = new_expr
            
        # Convert standard operators
        expr = re.sub(r'\bAND\b|\b\^\b|\b&\b', ' and ', expr)
        expr = re.sub(r'\bOR\b|\bv\b|\|', ' or ', expr)
        expr = re.sub(r'\bNOT\b|~', ' not ', expr)
        return expr

    def get_variables(self, expression):
        # Extract unique variable names like P, Q, R
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression)
        keywords = {'and', 'or', 'not', 'true', 'false', 'iff', 'implies', 'v', 'if', 'else'}
        return sorted(list(set(w for w in words if w.lower() not in keywords)))

    def generate_truth_table(self, expression, description=""):
        variables = self.get_variables(expression)
        combinations = list(itertools.product([True, False], repeat=len(variables)))
        
        print(f"\n[Task] {description}")
        print(f"Logic: {expression}")
        
        # Print Header
        header = " | ".join(variables) + " | Result"
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        
        results = []
        preprocessed = self.preprocess_expression(expression)
        
        for combo in combinations:
            assignments = dict(zip(variables, combo))
            try:
                # eval() executes the string as Python code using the T/F assignments
                res = eval(preprocessed, {"__builtins__": None}, assignments)
                results.append(res)
                row = " | ".join("T" if assignments[v] else "F" for v in variables)
                print(f"{row} | {'T' if res else 'F'}")
            except Exception as e:
                print(f"Error evaluating: {e}")
                return
        
        # Classify the logic
        if all(results): 
            print("Classification: Tautology (Always True)")
        elif not any(results): 
            print("Classification: Contradiction (Always False)")
        else: 
            print("Classification: Contingent (Mixed Results)")

if __name__ == "__main__":
    engine = PropositionalLogicEngine()
    
    # Example 1: Implication (If P then Q)
    engine.generate_truth_table("P -> Q", "Basic Implication")
    
    # Example 2: Law of Excluded Middle (Tautology)
    engine.generate_truth_table("P OR NOT P", "Excluded Middle")
    
    # Example 3: Natural Language translation from your list
    # "I am a rock and I am an island" -> P AND Q
    engine.generate_truth_table("P AND Q", "P: I am a rock, Q: I am an island")
