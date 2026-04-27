"""
Advanced First Order Logic - Knowledge Bases and Inference
Implements knowledge base management and various inference techniques.
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import re


@dataclass
class Fact:
    """Represents a fact in the knowledge base."""
    
    predicate: str
    args: List[str]
    
    def __repr__(self):
        return f"{self.predicate}({', '.join(self.args)})"
    
    def __hash__(self):
        return hash((self.predicate, tuple(self.args)))
    
    def __eq__(self, other):
        return isinstance(other, Fact) and self.predicate == other.predicate and self.args == other.args


@dataclass
class Rule:
    """Represents a rule: premises -> conclusion."""
    
    premises: List[Fact]
    conclusion: Fact
    
    def __repr__(self):
        premises_str = " ∧ ".join(str(p) for p in self.premises)
        return f"{premises_str} → {self.conclusion}"


class KnowledgeBase:
    """Manages facts and rules in a knowledge base."""
    
    def __init__(self):
        self.facts: Set[Fact] = set()
        self.rules: List[Rule] = []
    
    def add_fact(self, fact: Fact):
        """Add a fact to the knowledge base."""
        self.facts.add(fact)
    
    def add_rule(self, rule: Rule):
        """Add a rule to the knowledge base."""
        self.rules.append(rule)
    
    def add_fact_string(self, fact_str: str):
        """Add a fact from string representation."""
        # Parse "predicate(arg1, arg2, ...)"
        match = re.match(r'(\w+)\((.*)\)', fact_str.strip())
        if match:
            predicate = match.group(1)
            args = [arg.strip() for arg in match.group(2).split(',')]
            self.add_fact(Fact(predicate, args))
    
    def add_rule_string(self, rule_str: str):
        """Add a rule from string representation."""
        # Parse "premise1 & premise2 & ... -> conclusion"
        if '->' not in rule_str:
            raise ValueError("Invalid rule format")
        
        premises_str, conclusion_str = rule_str.split('->')
        
        # Parse premises
        premise_strs = [p.strip() for p in premises_str.split('&')]
        premises = []
        
        for p_str in premise_strs:
            match = re.match(r'(\w+)\((.*)\)', p_str.strip())
            if match:
                predicate = match.group(1)
                args = [arg.strip() for arg in match.group(2).split(',')]
                premises.append(Fact(predicate, args))
        
        # Parse conclusion
        match = re.match(r'(\w+)\((.*)\)', conclusion_str.strip())
        if match:
            predicate = match.group(1)
            args = [arg.strip() for arg in match.group(2).split(',')]
            conclusion = Fact(predicate, args)
            
            self.add_rule(Rule(premises, conclusion))
    
    def get_facts_with_predicate(self, predicate: str) -> Set[Fact]:
        """Get all facts with a given predicate."""
        return {f for f in self.facts if f.predicate == predicate}
    
    def __repr__(self):
        result = "Knowledge Base:\n"
        result += "Facts:\n"
        for fact in self.facts:
            result += f"  {fact}\n"
        result += "Rules:\n"
        for rule in self.rules:
            result += f"  {rule}\n"
        return result


class ForwardChainingInference:
    """Forward chaining inference engine."""
    
    @staticmethod
    def infer(kb: KnowledgeBase) -> Set[Fact]:
        """
        Perform forward chaining inference.
        
        Args:
            kb: Knowledge base
            
        Returns:
            Set of all derived facts
        """
        derived = set(kb.facts)
        new_facts = True
        
        while new_facts:
            new_facts = False
            
            for rule in kb.rules:
                # Check if all premises are in derived facts
                if all(ForwardChainingInference._matches(p, derived) for p in rule.premises):
                    if rule.conclusion not in derived:
                        derived.add(rule.conclusion)
                        new_facts = True
        
        return derived
    
    @staticmethod
    def _matches(fact: Fact, derived_facts: Set[Fact]) -> bool:
        """Check if a fact or its instance is in derived facts."""
        # Direct match
        if fact in derived_facts:
            return True
        
        # Check if any derived fact matches the pattern
        for derived_fact in derived_facts:
            if derived_fact.predicate == fact.predicate and len(derived_fact.args) == len(fact.args):
                # For simplicity, check direct argument match
                if derived_fact.args == fact.args:
                    return True
        
        return False


class BackwardChainingInference:
    """Backward chaining inference engine."""
    
    @staticmethod
    def prove(kb: KnowledgeBase, goal: Fact) -> bool:
        """
        Prove a goal using backward chaining.
        
        Args:
            kb: Knowledge base
            goal: Goal fact to prove
            
        Returns:
            True if goal can be proved, False otherwise
        """
        return BackwardChainingInference._prove_recursive(kb, goal, set())
    
    @staticmethod
    def _prove_recursive(kb: KnowledgeBase, goal: Fact, visited: Set[Fact]) -> bool:
        """Recursive backward chaining."""
        if goal in visited:
            return False
        
        visited.add(goal)
        
        # Check if goal is in facts
        if goal in kb.facts:
            return True
        
        # Check if goal can be derived from rules
        for rule in kb.rules:
            if rule.conclusion.predicate == goal.predicate:
                # Check if all premises can be proved
                all_premises_proved = True
                for premise in rule.premises:
                    if not BackwardChainingInference._prove_recursive(kb, premise, visited):
                        all_premises_proved = False
                        break
                
                if all_premises_proved:
                    return True
        
        return False
    
    @staticmethod
    def find_proof(kb: KnowledgeBase, goal: Fact, depth: int = 0) -> Optional[List]:
        """Find and return proof path."""
        indent = "  " * depth
        
        if goal in kb.facts:
            return [f"{indent}✓ {goal} (fact)"]
        
        for rule in kb.rules:
            if rule.conclusion.predicate == goal.predicate:
                proof_paths = []
                all_premises_proved = True
                
                for premise in rule.premises:
                    sub_proof = BackwardChainingInference.find_proof(kb, premise, depth + 1)
                    if sub_proof:
                        proof_paths.extend(sub_proof)
                    else:
                        all_premises_proved = False
                        break
                
                if all_premises_proved:
                    result = [f"{indent}→ {goal} from rule: {rule}"]
                    result.extend(proof_paths)
                    return result
        
        return None


class ResolutionInference:
    """Resolution-based inference for FOL."""
    
    @staticmethod
    def convert_to_cnf(facts: List[Fact]) -> List[Set[Tuple]]:
        """Convert facts to CNF format."""
        # Simplified - represent each fact as a clause
        cnf = []
        for fact in facts:
            # Each fact is a positive literal
            cnf.append({(False, (fact.predicate, tuple(fact.args)))})
        return cnf
    
    @staticmethod
    def resolve(clause1: Set[Tuple], clause2: Set[Tuple]) -> Optional[Set[Tuple]]:
        """Attempt resolution between two clauses."""
        # Find complementary literals
        for lit1 in clause1:
            negated1, pred1 = lit1
            for lit2 in clause2:
                negated2, pred2 = lit2
                
                # Check if literals are complementary
                if negated1 != negated2 and pred1 == pred2:
                    # Create resolvent
                    resolvent = (clause1 - {lit1}) | (clause2 - {lit2})
                    return resolvent if resolvent else None
        
        return None


class SimpleQueryEngine:
    """Simple query engine for knowledge base."""
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.inference_method = 'forward'  # or 'backward'
    
    def query(self, goal: Fact) -> bool:
        """Query if a goal can be proved."""
        if self.inference_method == 'forward':
            derived = ForwardChainingInference.infer(self.kb)
            return goal in derived
        else:
            return BackwardChainingInference.prove(self.kb, goal)
    
    def explain(self, goal: Fact):
        """Explain how a goal was proved."""
        proof = BackwardChainingInference.find_proof(self.kb, goal)
        if proof:
            print(f"\nProof for {goal}:")
            for line in proof:
                print(line)
        else:
            print(f"\nCannot prove {goal}")


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("KNOWLEDGE BASE AND INFERENCE")
    print("="*60)
    
    # Create knowledge base
    kb = KnowledgeBase()
    
    # Add facts
    print("\n1. Adding Facts:")
    print("-" * 60)
    
    kb.add_fact_string("Parent(Tom, Bob)")
    kb.add_fact_string("Parent(Tom, Liz)")
    kb.add_fact_string("Parent(Bob, Ann)")
    kb.add_fact_string("Parent(Bob, Pat)")
    kb.add_fact_string("Parent(Liz, Joe)")
    
    print("Added facts:")
    for fact in kb.facts:
        print(f"  {fact}")
    
    # Add rules
    print("\n2. Adding Rules:")
    print("-" * 60)
    
    kb.add_rule_string("Parent(X, Y) -> Ancestor(X, Y)")
    kb.add_rule_string("Parent(X, Y) & Ancestor(Y, Z) -> Ancestor(X, Z)")
    
    print("Added rules:")
    for rule in kb.rules:
        print(f"  {rule}")
    
    # Forward chaining
    print("\n3. Forward Chaining Inference:")
    print("-" * 60)
    
    derived = ForwardChainingInference.infer(kb)
    print("Derived facts:")
    for fact in derived:
        if fact not in kb.facts:
            print(f"  {fact} (derived)")
    
    # Query and explain
    print("\n4. Query and Explanation:")
    print("-" * 60)
    
    engine = SimpleQueryEngine(kb)
    
    # Test queries
    goal1 = Fact("Ancestor", ["Tom", "Bob"])
    goal2 = Fact("Ancestor", ["Tom", "Ann"])
    goal3 = Fact("Ancestor", ["Tom", "Joe"])
    
    engine.inference_method = 'backward'
    
    engine.explain(goal1)
    engine.explain(goal2)
    engine.explain(goal3)
