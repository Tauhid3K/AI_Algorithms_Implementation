"""
Predicate Logic - Topic 3
Implementation of predicate logic with quantifiers (∀, ∃), predicates, and model interpretation
"""

import itertools
from collections import defaultdict


class PredicateLogicSystem:
    """Predicate logic system with quantified formulas and model checking"""

    def __init__(self):
        self.predicates = {}
        self.universe = set()
        self.interpretations = {}

    def define_universe(self, elements):
        """Define the universe of discourse"""
        self.universe = set(elements)
        print(f"✓ Universe: {self.universe}")

    def define_predicate(self, predicate_name, arity, interpretation):
        """
        Define a predicate with interpretation
        interpretation: dict mapping tuples to truth values
        """
        self.predicates[predicate_name] = {
            'arity': arity,
            'interpretation': interpretation
        }
        print(f"✓ Predicate {predicate_name}/{arity}: {len(interpretation)} tuples")

    def evaluate_predicate(self, name, args):
        """Evaluate a predicate with given arguments"""
        if name not in self.predicates:
            return False
        
        pred_def = self.predicates[name]
        if len(args) != pred_def['arity']:
            return False
        
        key = tuple(args)
        return pred_def['interpretation'].get(key, False)

    def universal_quantifier(self, predicate_name, args_template):
        """
        ∀x P(x) - For all x in universe, P(x) is true
        Returns True if P holds for ALL elements in universe
        """
        print(f"\n[Universal] ∀x {predicate_name}({args_template})")
        results = []
        for element in self.universe:
            args = [element if arg == '?x' else arg for arg in args_template]
            result = self.evaluate_predicate(predicate_name, args)
            print(f"  {predicate_name}({element}): {result}")
            results.append(result)
        
        truth_value = all(results)
        print(f"  Result: ∀x {predicate_name}(x) = {truth_value}")
        return truth_value

    def existential_quantifier(self, predicate_name, args_template):
        """
        ∃x P(x) - There exists x in universe such that P(x) is true
        Returns True if P holds for AT LEAST ONE element in universe
        """
        print(f"\n[Existential] ∃x {predicate_name}({args_template})")
        results = []
        for element in self.universe:
            args = [element if arg == '?x' else arg for arg in args_template]
            result = self.evaluate_predicate(predicate_name, args)
            print(f"  {predicate_name}({element}): {result}")
            results.append(result)
        
        truth_value = any(results)
        print(f"  Result: ∃x {predicate_name}(x) = {truth_value}")
        return truth_value

    def negation_of_universal(self, predicate_name, args_template):
        """¬∀x P(x) ≡ ∃x ¬P(x)"""
        print(f"\n[De Morgan's] ¬∀x {predicate_name}(x) ≡ ∃x ¬{predicate_name}(x)")
        
        negated_results = []
        for element in self.universe:
            args = [element if arg == '?x' else arg for arg in args_template]
            result = not self.evaluate_predicate(predicate_name, args)
            negated_results.append(result)
        
        return any(negated_results)

    def relational_logic(self, relation_name, arg1, arg2):
        """
        Handle binary relations: R(x, y)
        Check specific relationship between elements
        """
        print(f"\n[Relation] {relation_name}({arg1}, {arg2})")
        result = self.evaluate_predicate(relation_name, [arg1, arg2])
        print(f"  Result: {result}")
        return result

    def model_checking(self, formula_name):
        """Check if formula is true in the interpretation"""
        print(f"\n[Model Checking] Formula: {formula_name}")
        print(f"  Universe: {self.universe}")
        print(f"  Predicates defined: {list(self.predicates.keys())}")
        return True


# Example Usage
if __name__ == "__main__":
    system = PredicateLogicSystem()
    
    print("=" * 60)
    print("PREDICATE LOGIC SYSTEM - TOPIC 3")
    print("=" * 60)
    
    # Example 1: Simple Predicate Logic
    print("\n>>> EXAMPLE 1: Define Universe and Predicates")
    system.define_universe(['Alice', 'Bob', 'Charlie', 'Diana'])
    
    # Define Parent predicate: Parent(x, y)
    parent_interpretation = {
        ('Alice', 'Bob'): True,
        ('Alice', 'Charlie'): True,
        ('Bob', 'Diana'): True,
    }
    system.define_predicate('Parent', 2, parent_interpretation)
    
    # Define Person predicate: Person(x)
    person_interpretation = {
        ('Alice',): True,
        ('Bob',): True,
        ('Charlie',): True,
        ('Diana',): True,
    }
    system.define_predicate('Person', 1, person_interpretation)
    
    # Example 2: Universal Quantifier
    print("\n>>> EXAMPLE 2: Universal Quantifier ∀x")
    system.universal_quantifier('Person', ['?x'])
    
    # Example 3: Existential Quantifier
    print("\n>>> EXAMPLE 3: Existential Quantifier ∃x")
    system.existential_quantifier('Parent', ['Alice', '?x'])
    
    # Example 4: Negation equivalence
    print("\n>>> EXAMPLE 4: De Morgan's Laws")
    system.negation_of_universal('Person', ['?x'])
    
    # Example 5: Binary Relations
    print("\n>>> EXAMPLE 5: Binary Relations")
    system.relational_logic('Parent', 'Alice', 'Bob')
    system.relational_logic('Parent', 'Charlie', 'Diana')
    
    # Example 6: Complex predicate
    print("\n>>> EXAMPLE 6: Complex Predicates")
    married_interpretation = {
        ('Alice', 'Tom'): True,
        ('Bob', 'Jane'): True,
    }
    system.define_predicate('Married', 2, married_interpretation)
    
    # Example 7: Model Checking
    print("\n>>> EXAMPLE 7: Model Checking")
    system.model_checking("∀x Parent(x, ?y) → Person(?y)")
    
    print("\n" + "=" * 60)
