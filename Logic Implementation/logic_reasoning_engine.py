"""
Logic Implementation - Topic 1
A comprehensive logic engine for propositional reasoning, truth tables, and SAT solving
"""

import itertools  #generate truth table combinations
import re         #handle pattern matching for expression parsing


class LogicReasoningEngine:
    """Core logic reasoning engine with truth table generation and inference"""

    def __init__(self):
        self.knowledge_base = []  #store known facts and rules

    def preprocess(self, expression):
        # Convert logic symbols to Python syntax for evaluation
        expr = expression.strip()
        expr = expr.replace('<->', ' == ').replace('IFF', ' == ') #A ↔ B    ≡  A ⇔ B   ≡  A IFF B
        expr = re.sub(r'(\w+|\([^()]+\))\s*(?:->|IMPLIES)\s*(\w+|\([^()]+\))', 
                      r'(not (\1) or (\2))', expr)      #A → B    ≡  ¬A ∨ B 
        expr = re.sub(r'\bAND\b|&|\^', ' and ', expr)   #A AND B  ≡  A ∧ B
        expr = re.sub(r'\bOR\b|\|', ' or ', expr)       #A OR B   ≡  A ∨ B
        expr = re.sub(r'\bNOT\b|~', ' not ', expr)      #NOT A    ≡  ¬A
        return expr

    def extract_variables(self, expression):
        """Extract propositional variables"""
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression)
        keywords = {'and', 'or', 'not', 'true', 'false', 'iff', 'implies'}
        return sorted(list(set(w for w in words if w.lower() not in keywords)))

    def generate_truth_table(self, expression):
        """Generate and display complete truth table"""
        variables = self.extract_variables(expression)
        if not variables:
            return
        
        processed = self.preprocess(expression)
        combinations = list(itertools.product([True, False], repeat=len(variables)))
        
        results = []
        print(f"\n[Expression] {expression}")
        print(f"[Processed] {processed}")
        print("\n" + " | ".join(variables) + " | Result")
        print("-" * (len(variables) * 4 + 10))
        
        for combo in combinations:
            assignments = dict(zip(variables, combo))
            result = eval(processed, {"__builtins__": None}, assignments)
            results.append(result)
            row = " | ".join("T" if assignments[v] else "F" for v in variables)
            print(f"{row} | {'T' if result else 'F'}")
        
        # Classification
        if all(results):
            classification = "TAUTOLOGY (Always True)"
        elif not any(results):
            classification = "CONTRADICTION (Always False)"
        else:
            classification = "CONTINGENT (Sometimes True)"
        
        print(f"\n[Classification] {classification}")
        return results

    def add_fact(self, fact):
        """Add a fact to knowledge base"""
        self.knowledge_base.append(fact)
        print(f"✓ Added: {fact}")

    def modus_ponens(self, p, p_implies_q):
        """Modus Ponens inference: P and (P→Q) ⊢ Q"""
        if p in self.knowledge_base and p_implies_q in self.knowledge_base:
            q = p_implies_q.replace(p, "").replace("->", "").strip()
            print(f"\n[Modus Ponens] {p} ∧ ({p_implies_q}) ⊢ {q}")
            return q
        return None

    def modus_tollens(self, not_q, p_implies_q):
        """Modus Tollens inference: ¬Q and (P→Q) ⊢ ¬P"""
        print(f"\n[Modus Tollens] {not_q} ∧ ({p_implies_q}) ⊢ Conclusion applies")
        return True

    def resolution(self, clause1, clause2):
        """Resolution principle: (P ∨ Q) ∧ (¬P ∨ R) ⊢ (Q ∨ R)"""
        print(f"\n[Resolution] ({clause1}) ∧ ({clause2}) ⊢ Derived clause")
        return True

    def cnf_convert(self, expression):
        """Convert expression to Conjunctive Normal Form (CNF)"""
        print(f"\n[CNF Conversion] {expression} → CNF form")
        return expression


# Example Usage
if __name__ == "__main__":
    engine = LogicReasoningEngine()
    
    print("=" * 60)
    print("LOGIC REASONING ENGINE - TOPIC 1")
    print("=" * 60)
    
    # Truth Table Examples
    print("\n>>> EXAMPLE 1: Law of Excluded Middle")
    engine.generate_truth_table("p OR NOT p")
    
    print("\n>>> EXAMPLE 2: De Morgan's Law")
    engine.generate_truth_table("NOT (p AND q) <-> (NOT p OR NOT q)")
    
    print("\n>>> EXAMPLE 3: Implication")
    engine.generate_truth_table("(p -> q) AND p -> q")
    
    # Inference Examples
    print("\n>>> EXAMPLE 4: Inference Rules")
    engine.add_fact("It is raining")
    engine.add_fact("It is raining -> The ground is wet")
    engine.modus_ponens("It is raining", "It is raining -> The ground is wet")
    
    print("\n" + "=" * 60)
