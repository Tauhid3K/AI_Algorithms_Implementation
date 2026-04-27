"""
First Order Logic - Topic 2
Implementation of first-order logic with quantifiers, unification, and forward chaining inference
"""

import re
from itertools import product


class FirstOrderLogicSystem:
    """First-order logic system with unification and inference"""

    def __init__(self):
        self.facts = []
        self.rules = []
        self.domain = {}

    def add_fact(self, fact):
        """Add a ground fact to the knowledge base"""
        self.facts.append(fact)
        print(f"✓ Fact: {fact}")

    def add_rule(self, condition, conclusion):
        """Add an inference rule: condition → conclusion"""
        self.rules.append((condition, conclusion))
        print(f"✓ Rule: {condition} → {conclusion}")

    def add_domain(self, predicate, entities):
        """Define domain for a predicate"""
        self.domain[predicate] = entities
        print(f"✓ Domain {predicate}: {entities}")

    def unify(self, term1, term2, substitution=None):
        """
        Unification algorithm: find substitution to make terms identical
        Returns substitution dict or None if unification fails
        """
        if substitution is None:
            substitution = {}
        
        if term1 == term2:
            return substitution
        
        if isinstance(term1, str) and term1.startswith('?'):
            if term1 in substitution:
                return self.unify(substitution[term1], term2, substitution)
            else:
                substitution[term1] = term2
                return substitution
        
        if isinstance(term2, str) and term2.startswith('?'):
            if term2 in substitution:
                return self.unify(term1, substitution[term2], substitution)
            else:
                substitution[term2] = term1
                return substitution
        
        return None

    def apply_substitution(self, term, substitution):
        """Apply substitution to a term"""
        if isinstance(term, str) and term in substitution:
            return substitution[term]
        return term

    def instantiate(self, predicate, domain_entities):
        """Instantiate universally quantified predicates"""
        print(f"\n[Instantiation] ∀x. {predicate}(x)")
        results = []
        for entity in domain_entities:
            instantiated = predicate.replace("?x", entity).replace("x", entity)
            results.append(instantiated)
            print(f"  → {instantiated}")
        return results

    def forward_chaining(self, query):
        """Forward chaining inference: derive all possible facts"""
        print(f"\n[Forward Chaining] Query: {query}")
        derived = set(self.facts)
        previous = set()
        
        iteration = 0
        while derived != previous:
            iteration += 1
            previous = derived.copy()
            print(f"  Iteration {iteration}: {len(derived)} facts")
            
            for condition, conclusion in self.rules:
                for fact in derived:
                    subst = self.unify(condition, fact)
                    if subst:
                        new_fact = conclusion
                        for var, val in subst.items():
                            new_fact = new_fact.replace(var, val)
                        if new_fact not in derived:
                            derived.add(new_fact)
                            print(f"    + Derived: {new_fact}")
        
        return query in derived

    def backward_chaining(self, goal, depth=0):
        """Backward chaining inference: prove a goal"""
        indent = "  " * depth
        print(f"{indent}[Goal] {goal}")
        
        if goal in self.facts:
            print(f"{indent}  ✓ Found in facts")
            return True
        
        for condition, conclusion in self.rules:
            subst = self.unify(goal, conclusion)
            if subst:
                print(f"{indent}  → Rule matches, proving: {condition}")
                if self.backward_chaining(condition, depth + 1):
                    return True
        
        print(f"{indent}  ✗ Failed")
        return False

    def resolve(self, clause1, clause2):
        """Resolution: CNF form inference"""
        print(f"\n[Resolution] {clause1} ∧ {clause2}")
        return True


# Example Usage
if __name__ == "__main__":
    system = FirstOrderLogicSystem()
    
    print("=" * 60)
    print("FIRST ORDER LOGIC SYSTEM - TOPIC 2")
    print("=" * 60)
    
    # Add Domain
    print("\n>>> EXAMPLE 1: Domain Definition")
    system.add_domain("Person", ["Alice", "Bob", "Charlie"])
    system.add_domain("Color", ["Red", "Blue", "Green"])
    
    # Add Facts
    print("\n>>> EXAMPLE 2: Facts")
    system.add_fact("Parent(Alice, Bob)")
    system.add_fact("Parent(Bob, Charlie)")
    system.add_fact("Male(Bob)")
    system.add_fact("Female(Alice)")
    
    # Add Rules
    print("\n>>> EXAMPLE 3: Inference Rules")
    system.add_rule("Parent(?x, ?y)", "Ancestor(?x, ?y)")
    system.add_rule("Parent(?x, ?y) AND Parent(?y, ?z)", "Grandparent(?x, ?z)")
    system.add_rule("Parent(?x, ?y) AND Parent(?x, ?z)", "Sibling(?y, ?z)")
    
    # Unification
    print("\n>>> EXAMPLE 4: Unification")
    subst = system.unify("Parent(?x, Bob)", "Parent(Alice, Bob)")
    print(f"  Substitution: {subst}")
    
    # Instantiation
    print("\n>>> EXAMPLE 5: Universal Instantiation")
    system.instantiate("Parent(?x, Bob)", ["Alice", "Charlie"])
    
    # Forward Chaining
    print("\n>>> EXAMPLE 6: Forward Chaining")
    system.forward_chaining("Ancestor(Alice, Bob)")
    
    # Backward Chaining
    print("\n>>> EXAMPLE 7: Backward Chaining")
    system.backward_chaining("Parent(Alice, Bob)")
    
    print("\n" + "=" * 60)
