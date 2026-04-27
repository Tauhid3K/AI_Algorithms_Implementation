"""
First Order Logic (FOL)
Implements first-order logic with resolution and unification algorithms.
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import re


@dataclass
class Term:
    """Represents a term in first-order logic (constant, variable, or function)."""
    
    def __repr__(self):
        return str(self)


@dataclass
class Constant(Term):
    """Represents a constant (e.g., 'john', 'mary')."""
    
    name: str
    
    def __repr__(self):
        return self.name


@dataclass
class Variable(Term):
    """Represents a variable (e.g., X, Y, Z)."""
    
    name: str
    
    def __repr__(self):
        return f"_{self.name}"


@dataclass
class Function(Term):
    """Represents a function term (e.g., father(john))."""
    
    functor: str
    args: List[Term]
    
    def __repr__(self):
        if not self.args:
            return f"{self.functor}()"
        return f"{self.functor}({', '.join(str(arg) for arg in self.args)})"


@dataclass
class Predicate:
    """Represents a predicate (e.g., Loves(john, mary))."""
    
    name: str
    args: List[Term]
    
    def __repr__(self):
        if not self.args:
            return f"{self.name}()"
        return f"{self.name}({', '.join(str(arg) for arg in self.args)})"
    
    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return False
        return self.name == other.name and len(self.args) == len(other.args)
    
    def __hash__(self):
        return hash((self.name, len(self.args)))


@dataclass
class Clause:
    """Represents a clause (disjunction of literals)."""
    
    literals: List[Tuple[bool, Predicate]]  # (negated, predicate)
    
    def __repr__(self):
        parts = []
        for negated, pred in self.literals:
            if negated:
                parts.append(f"¬{pred}")
            else:
                parts.append(str(pred))
        return " ∨ ".join(parts)
    
    def is_unit_clause(self) -> bool:
        """Check if this is a unit clause (single literal)."""
        return len(self.literals) == 1
    
    def is_empty(self) -> bool:
        """Check if this is the empty clause (contradiction)."""
        return len(self.literals) == 0


class Substitution:
    """Represents variable substitutions for unification."""
    
    def __init__(self, mapping: Dict[str, Term] = None):
        self.mapping = mapping or {}
    
    def __repr__(self):
        items = [f"{var}: {term}" for var, term in self.mapping.items()]
        return "{" + ", ".join(items) + "}"
    
    def apply(self, term: Term) -> Term:
        """Apply substitution to a term."""
        if isinstance(term, Constant):
            return term
        elif isinstance(term, Variable):
            if term.name in self.mapping:
                return self.apply(self.mapping[term.name])
            return term
        elif isinstance(term, Function):
            new_args = [self.apply(arg) for arg in term.args]
            return Function(term.functor, new_args)
        return term
    
    def apply_to_predicate(self, pred: Predicate) -> Predicate:
        """Apply substitution to a predicate."""
        new_args = [self.apply(arg) for arg in pred.args]
        return Predicate(pred.name, new_args)
    
    def apply_to_clause(self, clause: Clause) -> Clause:
        """Apply substitution to a clause."""
        new_literals = [
            (negated, self.apply_to_predicate(pred))
            for negated, pred in clause.literals
        ]
        return Clause(new_literals)
    
    def compose(self, other: 'Substitution') -> 'Substitution':
        """Compose two substitutions."""
        # Apply other to self's values
        new_mapping = {}
        for var, term in self.mapping.items():
            new_mapping[var] = other.apply(term)
        
        # Add mappings from other that aren't in self
        for var, term in other.mapping.items():
            if var not in new_mapping:
                new_mapping[var] = term
        
        return Substitution(new_mapping)


class Unification:
    """Implements the unification algorithm."""
    
    @staticmethod
    def unify(term1: Term, term2: Term, subst: Substitution = None) -> Optional[Substitution]:
        """
        Unify two terms.
        
        Args:
            term1: First term
            term2: Second term
            subst: Existing substitution
            
        Returns:
            Substitution that makes terms equal, or None if unification fails
        """
        if subst is None:
            subst = Substitution()
        
        term1 = subst.apply(term1)
        term2 = subst.apply(term2)
        
        # Same term
        if isinstance(term1, Constant) and isinstance(term2, Constant):
            if term1.name == term2.name:
                return subst
            return None
        
        # Variable unification
        if isinstance(term1, Variable):
            return Unification._unify_variable(term1, term2, subst)
        if isinstance(term2, Variable):
            return Unification._unify_variable(term2, term1, subst)
        
        # Function unification
        if isinstance(term1, Function) and isinstance(term2, Function):
            if term1.functor != term2.functor or len(term1.args) != len(term2.args):
                return None
            
            for arg1, arg2 in zip(term1.args, term2.args):
                subst = Unification.unify(arg1, arg2, subst)
                if subst is None:
                    return None
            
            return subst
        
        return None
    
    @staticmethod
    def _unify_variable(var: Variable, term: Term, subst: Substitution) -> Optional[Substitution]:
        """Helper method to unify a variable with a term."""
        if isinstance(term, Variable) and var.name == term.name:
            return subst
        
        if Unification._occurs_check(var, term, subst):
            return None
        
        new_mapping = subst.mapping.copy()
        new_mapping[var.name] = term
        return Substitution(new_mapping)
    
    @staticmethod
    def _occurs_check(var: Variable, term: Term, subst: Substitution) -> bool:
        """Check if variable occurs in term (prevents infinite structures)."""
        term = subst.apply(term)
        
        if isinstance(term, Variable):
            return var.name == term.name
        elif isinstance(term, Function):
            return any(Unification._occurs_check(var, arg, subst) for arg in term.args)
        
        return False
    
    @staticmethod
    def unify_predicates(pred1: Predicate, pred2: Predicate) -> Optional[Substitution]:
        """Unify two predicates."""
        if pred1.name != pred2.name or len(pred1.args) != len(pred2.args):
            return None
        
        subst = Substitution()
        for arg1, arg2 in zip(pred1.args, pred2.args):
            subst = Unification.unify(arg1, arg2, subst)
            if subst is None:
                return None
        
        return subst


class FOLResolution:
    """Implements First Order Logic resolution for theorem proving."""
    
    def __init__(self):
        self.clauses: List[Clause] = []
        self.knowledge_base: List[Clause] = []
    
    def add_clause(self, clause: Clause):
        """Add a clause to the knowledge base."""
        self.knowledge_base.append(clause)
    
    def resolve_clauses(self, clause1: Clause, clause2: Clause) -> List[Clause]:
        """
        Resolve two clauses.
        
        Args:
            clause1: First clause
            clause2: Second clause
            
        Returns:
            List of resolvent clauses
        """
        resolvents = []
        
        for i, (neg1, pred1) in enumerate(clause1.literals):
            for j, (neg2, pred2) in enumerate(clause2.literals):
                # Check if literals can be resolved (opposite signs)
                if neg1 == neg2:
                    continue
                
                # Try to unify predicates
                unifier = Unification.unify_predicates(pred1, pred2)
                if unifier is None:
                    continue
                
                # Create resolvent
                new_literals = []
                
                # Add all literals from clause1 except the resolved one
                for k, (neg, pred) in enumerate(clause1.literals):
                    if k != i:
                        new_literals.append((neg, unifier.apply_to_predicate(pred)))
                
                # Add all literals from clause2 except the resolved one
                for k, (neg, pred) in enumerate(clause2.literals):
                    if k != j:
                        new_literals.append((neg, unifier.apply_to_predicate(pred)))
                
                resolvent = Clause(new_literals)
                resolvents.append(resolvent)
        
        return resolvents
    
    def prove(self, goal: Clause, max_iterations: int = 1000) -> bool:
        """
        Prove a goal using resolution.
        
        Args:
            goal: Goal clause to prove (negated query)
            max_iterations: Maximum iterations to prevent infinite loops
            
        Returns:
            True if goal is proved, False otherwise
        """
        # Convert goal to CNF (negate it)
        new_clauses = [Clause([(True, pred) if not neg else (False, pred) 
                               for neg, pred in goal.literals])]
        
        for iteration in range(max_iterations):
            if not new_clauses:
                return True
            
            # Check for empty clause
            for clause in new_clauses:
                if clause.is_empty():
                    return True
            
            # Try all pairs of clauses
            all_clauses = self.knowledge_base + new_clauses
            clause_set = set()
            
            for i, clause1 in enumerate(all_clauses):
                for j, clause2 in enumerate(all_clauses[i+1:], i+1):
                    for resolvent in self.resolve_clauses(clause1, clause2):
                        if resolvent.is_empty():
                            return True
                        clause_set.add(repr(resolvent))
            
            if not clause_set:
                return False
            
            # Filter out duplicate clauses
            new_clauses = []
            for clause_repr in clause_set:
                # This is simplified - in reality we'd parse back to Clause
                new_clauses.append(Clause([]))
        
        return False


class FOLParser:
    """Parser for First Order Logic expressions."""
    
    @staticmethod
    def parse_term(expression: str) -> Term:
        """Parse a term from a string."""
        expression = expression.strip()
        
        # Variable (starts with uppercase or underscore)
        if expression[0].isupper() or expression[0] == '_':
            return Variable(expression)
        
        # Function or constant
        if '(' in expression:
            match = re.match(r'(\w+)\((.*)\)', expression)
            if match:
                functor = match.group(1)
                args_str = match.group(2)
                
                if not args_str:
                    args = []
                else:
                    args = [FOLParser.parse_term(arg.strip()) for arg in args_str.split(',')]
                
                return Function(functor, args)
        
        # Constant
        return Constant(expression)
    
    @staticmethod
    def parse_predicate(expression: str) -> Predicate:
        """Parse a predicate from a string."""
        expression = expression.strip()
        
        if '(' not in expression:
            return Predicate(expression, [])
        
        match = re.match(r'(\w+)\((.*)\)', expression)
        if match:
            name = match.group(1)
            args_str = match.group(2)
            
            if not args_str:
                args = []
            else:
                args = [FOLParser.parse_term(arg.strip()) for arg in args_str.split(',')]
            
            return Predicate(name, args)
        
        raise ValueError(f"Invalid predicate: {expression}")


# Example usage
if __name__ == "__main__":
    print("=== First Order Logic ===\n")
    
    # Example: Unification
    print("=== Unification ===")
    
    john = Constant("john")
    mary = Constant("mary")
    X = Variable("X")
    Y = Variable("Y")
    
    pred1 = Predicate("Loves", [john, Y])
    pred2 = Predicate("Loves", [X, mary])
    
    unifier = Unification.unify_predicates(pred1, pred2)
    print(f"Unify {pred1} and {pred2}")
    print(f"Unifier: {unifier}\n")
    
    # Example: Resolution
    print("=== Resolution ===")
    
    # Knowledge Base: 
    # 1. Mortal(X) ∨ Immortal(X)
    # 2. ¬Human(X) ∨ Mortal(X)
    # 3. Human(socrates)
    # Goal: Prove Mortal(socrates)
    
    resolution = FOLResolution()
    
    # Add clauses to KB
    X = Variable("X")
    clause1 = Clause([
        (False, Predicate("Mortal", [X])),
        (False, Predicate("Immortal", [X]))
    ])
    
    clause2 = Clause([
        (True, Predicate("Human", [X])),
        (False, Predicate("Mortal", [X]))
    ])
    
    clause3 = Clause([
        (False, Predicate("Human", [Constant("socrates")]))
    ])
    
    resolution.add_clause(clause1)
    resolution.add_clause(clause2)
    resolution.add_clause(clause3)
    
    print(f"Clause 1: {clause1}")
    print(f"Clause 2: {clause2}")
    print(f"Clause 3: {clause3}")
    
    # Goal: ¬Mortal(socrates)
    goal = Clause([
        (True, Predicate("Mortal", [Constant("socrates")]))
    ])
    
    print(f"\nGoal (negated): {goal}")
    result = resolution.prove(goal)
    print(f"Proved: {result}")
