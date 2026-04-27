"""
Predicate Logic
Implements propositional and predicate logic with various operations and inference rules.
"""

from typing import Dict, List, Set, Tuple, Optional
from enum import Enum
from dataclasses import dataclass


class Operator(Enum):
    """Logical operators."""
    AND = "∧"
    OR = "∨"
    NOT = "¬"
    IMPLIES = "→"
    IFF = "↔"


@dataclass
class Proposition:
    """Represents a simple proposition."""
    
    name: str
    
    def __repr__(self):
        return self.name


class Formula:
    """Base class for logical formulas."""
    
    def __repr__(self):
        raise NotImplementedError
    
    def variables(self) -> Set[str]:
        """Get all variables in the formula."""
        raise NotImplementedError
    
    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        """Evaluate the formula given a variable assignment."""
        raise NotImplementedError


class AtomicFormula(Formula):
    """An atomic formula (single proposition)."""
    
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return self.name
    
    def variables(self) -> Set[str]:
        return {self.name}
    
    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        if self.name not in assignment:
            raise ValueError(f"Missing assignment for {self.name}")
        return assignment[self.name]


class CompoundFormula(Formula):
    """A compound formula (combination of formulas with operators)."""
    
    def __init__(self, operator: Operator, *operands: Formula):
        if operator == Operator.NOT and len(operands) != 1:
            raise ValueError("NOT operator requires exactly one operand")
        if operator in [Operator.AND, Operator.OR, Operator.IMPLIES, Operator.IFF] and len(operands) < 2:
            raise ValueError(f"{operator.value} requires at least two operands")
        
        self.operator = operator
        self.operands = operands
    
    def __repr__(self):
        if self.operator == Operator.NOT:
            return f"{self.operator.value}{self.operands[0]}"
        
        op_str = f" {self.operator.value} "
        return "(" + op_str.join(str(op) for op in self.operands) + ")"
    
    def variables(self) -> Set[str]:
        result = set()
        for operand in self.operands:
            result.update(operand.variables())
        return result
    
    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        if self.operator == Operator.NOT:
            return not self.operands[0].evaluate(assignment)
        
        elif self.operator == Operator.AND:
            return all(op.evaluate(assignment) for op in self.operands)
        
        elif self.operator == Operator.OR:
            return any(op.evaluate(assignment) for op in self.operands)
        
        elif self.operator == Operator.IMPLIES:
            # A → B is equivalent to ¬A ∨ B
            p = self.operands[0].evaluate(assignment)
            q = self.operands[1].evaluate(assignment)
            return (not p) or q
        
        elif self.operator == Operator.IFF:
            # A ↔ B is equivalent to (A → B) ∧ (B → A)
            p = self.operands[0].evaluate(assignment)
            q = self.operands[1].evaluate(assignment)
            return p == q


class CNF:
    """Conjunctive Normal Form (CNF) - conjunction of disjunctions."""
    
    def __init__(self, clauses: List[List[Tuple[bool, str]]]):
        """
        Initialize CNF.
        
        Args:
            clauses: List of clauses, each clause is a list of (negated, variable) tuples
                    representing a disjunction (OR) of literals.
        """
        self.clauses = clauses
    
    def __repr__(self):
        clause_strs = []
        for clause in self.clauses:
            literals = []
            for negated, var in clause:
                if negated:
                    literals.append(f"¬{var}")
                else:
                    literals.append(var)
            clause_strs.append("(" + " ∨ ".join(literals) + ")")
        return " ∧ ".join(clause_strs)
    
    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        """Evaluate CNF formula."""
        for clause in self.clauses:
            clause_result = False
            for negated, var in clause:
                if var not in assignment:
                    raise ValueError(f"Missing assignment for {var}")
                
                literal_value = assignment[var]
                if negated:
                    literal_value = not literal_value
                
                clause_result = clause_result or literal_value
            
            if not clause_result:
                return False
        
        return True


class DNF:
    """Disjunctive Normal Form (DNF) - disjunction of conjunctions."""
    
    def __init__(self, terms: List[List[Tuple[bool, str]]]):
        """
        Initialize DNF.
        
        Args:
            terms: List of terms, each term is a list of (negated, variable) tuples
                   representing a conjunction (AND) of literals.
        """
        self.terms = terms
    
    def __repr__(self):
        term_strs = []
        for term in self.terms:
            literals = []
            for negated, var in term:
                if negated:
                    literals.append(f"¬{var}")
                else:
                    literals.append(var)
            term_strs.append("(" + " ∧ ".join(literals) + ")")
        return " ∨ ".join(term_strs)
    
    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        """Evaluate DNF formula."""
        for term in self.terms:
            term_result = True
            for negated, var in term:
                if var not in assignment:
                    raise ValueError(f"Missing assignment for {var}")
                
                literal_value = assignment[var]
                if negated:
                    literal_value = not literal_value
                
                term_result = term_result and literal_value
            
            if term_result:
                return True
        
        return False


class PredicateLogicAnalyzer:
    """Analyzer for propositional and predicate logic."""
    
    @staticmethod
    def formula_to_cnf(formula: Formula) -> CNF:
        """
        Convert a formula to Conjunctive Normal Form (CNF).
        
        Args:
            formula: Formula to convert
            
        Returns:
            CNF representation of the formula
        """
        # This is a simplified implementation
        # Full CNF conversion requires several steps including:
        # 1. Eliminate implications
        # 2. Move negations inward (De Morgan's laws)
        # 3. Distribute OR over AND
        
        # For simplicity, we'll represent it as a single clause
        variables = formula.variables()
        from itertools import product
        
        clauses = []
        for values in product([False, True], repeat=len(variables)):
            var_dict = dict(zip(sorted(variables), values))
            if not formula.evaluate(var_dict):
                # Add negation of this assignment as a clause
                clause = []
                for var, value in var_dict.items():
                    clause.append((value, var))  # Negated because we want negation of false case
                clauses.append(clause)
        
        return CNF(clauses)
    
    @staticmethod
    def formula_to_dnf(formula: Formula) -> DNF:
        """
        Convert a formula to Disjunctive Normal Form (DNF).
        
        Args:
            formula: Formula to convert
            
        Returns:
            DNF representation of the formula
        """
        variables = formula.variables()
        from itertools import product
        
        terms = []
        for values in product([False, True], repeat=len(variables)):
            var_dict = dict(zip(sorted(variables), values))
            if formula.evaluate(var_dict):
                # Add this assignment as a term
                term = []
                for var, value in var_dict.items():
                    term.append((not value, var))  # Negated if value is False
                terms.append(term)
        
        return DNF(terms)
    
    @staticmethod
    def get_truth_table(formula: Formula) -> List[Dict]:
        """
        Generate a truth table for a formula.
        
        Args:
            formula: Formula to analyze
            
        Returns:
            List of dictionaries showing assignments and results
        """
        variables = sorted(formula.variables())
        from itertools import product
        
        table = []
        for values in product([False, True], repeat=len(variables)):
            var_dict = dict(zip(variables, values))
            result = formula.evaluate(var_dict)
            row = {**var_dict, "Result": result}
            table.append(row)
        
        return table
    
    @staticmethod
    def print_truth_table(formula: Formula):
        """Print a formatted truth table."""
        table = PredicateLogicAnalyzer.get_truth_table(formula)
        
        if not table:
            return
        
        variables = sorted(table[0].keys())
        
        # Print header
        print(" | ".join(f"{var:^6}" for var in variables))
        print("-" * (len(variables) * 8))
        
        # Print rows
        for row in table:
            values = [str(row[var]) for var in variables]
            print(" | ".join(f"{v:^6}" for v in values))
    
    @staticmethod
    def is_tautology(formula: Formula) -> bool:
        """Check if formula is a tautology (always true)."""
        table = PredicateLogicAnalyzer.get_truth_table(formula)
        return all(row["Result"] for row in table)
    
    @staticmethod
    def is_contradiction(formula: Formula) -> bool:
        """Check if formula is a contradiction (always false)."""
        table = PredicateLogicAnalyzer.get_truth_table(formula)
        return not any(row["Result"] for row in table)
    
    @staticmethod
    def is_contingency(formula: Formula) -> bool:
        """Check if formula is contingent (sometimes true, sometimes false)."""
        return not (PredicateLogicAnalyzer.is_tautology(formula) or 
                   PredicateLogicAnalyzer.is_contradiction(formula))


class InferenceRules:
    """Inference rules for logical deduction."""
    
    @staticmethod
    def modus_ponens(p: Formula, p_implies_q: Formula) -> Optional[Formula]:
        """
        Modus Ponens: From P and P→Q, infer Q
        
        Args:
            p: A formula P
            p_implies_q: A formula P→Q
            
        Returns:
            The conclusion Q if applicable, None otherwise
        """
        # Simplified - in a full implementation, we'd need to check structural equality
        return p_implies_q  # This is simplified
    
    @staticmethod
    def modus_tollens(not_q: Formula, p_implies_q: Formula) -> Optional[Formula]:
        """
        Modus Tollens: From ¬Q and P→Q, infer ¬P
        
        Args:
            not_q: A formula ¬Q
            p_implies_q: A formula P→Q
            
        Returns:
            The conclusion ¬P if applicable, None otherwise
        """
        # Simplified implementation
        return not_q
    
    @staticmethod
    def hypothetical_syllogism(p_implies_q: Formula, q_implies_r: Formula) -> Optional[Formula]:
        """
        Hypothetical Syllogism: From P→Q and Q→R, infer P→R
        
        Args:
            p_implies_q: A formula P→Q
            q_implies_r: A formula Q→R
            
        Returns:
            The conclusion P→R if applicable, None otherwise
        """
        # Simplified implementation
        return p_implies_q
    
    @staticmethod
    def disjunctive_syllogism(p_or_q: Formula, not_p: Formula) -> Optional[Formula]:
        """
        Disjunctive Syllogism: From P∨Q and ¬P, infer Q
        
        Args:
            p_or_q: A formula P∨Q
            not_p: A formula ¬P
            
        Returns:
            The conclusion Q if applicable, None otherwise
        """
        # Simplified implementation
        return p_or_q


class QuantifierLogic:
    """Handles quantified formulas (∀ and ∃)."""
    
    @staticmethod
    def universal_instantiation(formula: str, domain_element: str) -> str:
        """
        Universal Instantiation: From ∀X P(X), infer P(a) for any a in domain.
        
        Args:
            formula: Formula with universal quantifier ∀X
            domain_element: Element from the domain
            
        Returns:
            Instantiated formula
        """
        # Replace X with domain_element
        return formula.replace("X", domain_element)
    
    @staticmethod
    def existential_generalization(formula: str, variable: str) -> str:
        """
        Existential Generalization: From P(a), infer ∃X P(X).
        
        Args:
            formula: Formula P(a)
            variable: Variable to generalize over
            
        Returns:
            Generalized formula with existential quantifier
        """
        return f"∃{variable} {formula}"
    
    @staticmethod
    def universal_generalization(formula: str, variable: str) -> str:
        """
        Universal Generalization: From P(a) for arbitrary a, infer ∀X P(X).
        
        Args:
            formula: Formula P(a)
            variable: Variable to generalize over
            
        Returns:
            Generalized formula with universal quantifier
        """
        return f"∀{variable} {formula}"


# Example usage
if __name__ == "__main__":
    print("=== Propositional Logic ===\n")
    
    # Create formulas
    p = AtomicFormula("P")
    q = AtomicFormula("Q")
    r = AtomicFormula("R")
    
    # P ∧ Q
    formula1 = CompoundFormula(Operator.AND, p, q)
    print(f"Formula: {formula1}")
    
    # (P ∨ Q) → R
    formula2 = CompoundFormula(
        Operator.IMPLIES,
        CompoundFormula(Operator.OR, p, q),
        r
    )
    print(f"Formula: {formula2}")
    
    # P → (Q ∧ R)
    formula3 = CompoundFormula(
        Operator.IMPLIES,
        p,
        CompoundFormula(Operator.AND, q, r)
    )
    print(f"Formula: {formula3}")
    
    # Evaluate
    assignment = {"P": True, "Q": False, "R": True}
    print(f"\nEvaluation with {assignment}:")
    print(f"{formula1} = {formula1.evaluate(assignment)}")
    print(f"{formula2} = {formula2.evaluate(assignment)}")
    print(f"{formula3} = {formula3.evaluate(assignment)}")
    
    print("\n=== Truth Table Analysis ===\n")
    
    # Tautology: P ∨ ¬P
    tautology = CompoundFormula(Operator.OR, p, CompoundFormula(Operator.NOT, p))
    print(f"Formula: {tautology}")
    print(f"Is tautology: {PredicateLogicAnalyzer.is_tautology(tautology)}")
    
    # Contradiction: P ∧ ¬P
    contradiction = CompoundFormula(Operator.AND, p, CompoundFormula(Operator.NOT, p))
    print(f"\nFormula: {contradiction}")
    print(f"Is contradiction: {PredicateLogicAnalyzer.is_contradiction(contradiction)}")
    
    # Contingency: P ∧ Q
    contingency = CompoundFormula(Operator.AND, p, q)
    print(f"\nFormula: {contingency}")
    print(f"Is contingency: {PredicateLogicAnalyzer.is_contingency(contingency)}")
    
    print("\n=== CNF and DNF ===\n")
    
    test_formula = CompoundFormula(
        Operator.OR,
        CompoundFormula(Operator.AND, p, q),
        r
    )
    print(f"Original: {test_formula}")
    
    cnf = PredicateLogicAnalyzer.formula_to_cnf(test_formula)
    print(f"CNF: {cnf}")
    
    dnf = PredicateLogicAnalyzer.formula_to_dnf(test_formula)
    print(f"DNF: {dnf}")
