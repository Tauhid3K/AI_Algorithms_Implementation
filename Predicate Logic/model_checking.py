"""
Advanced Predicate Logic - Model Checking and Semantic Analysis
Implements model checking and semantic validation for logical formulas.
"""

from typing import Dict, List, Set, Tuple, Callable
from enum import Enum
import itertools


class Operator(Enum):
    """Logical operators."""
    AND = "∧"
    OR = "∨"
    NOT = "¬"
    IMPLIES = "→"
    IFF = "↔"
    UNIVERSAL = "∀"
    EXISTENTIAL = "∃"


class Term:
    """Represents a term in predicate logic."""
    pass


class Variable(Term):
    """Variable term."""
    
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name


class Constant(Term):
    """Constant term."""
    
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Constant) and self.name == other.name


class Predicate(Term):
    """Predicate with arguments."""
    
    def __init__(self, name: str, args: List[Term] = None):
        self.name = name
        self.args = args or []
    
    def __repr__(self):
        if not self.args:
            return f"{self.name}()"
        return f"{self.name}({', '.join(str(arg) for arg in self.args)})"
    
    def __hash__(self):
        return hash((self.name, tuple(self.args)))
    
    def __eq__(self, other):
        return (isinstance(other, Predicate) and 
                self.name == other.name and 
                self.args == other.args)


class Formula:
    """Base class for formulas."""
    pass


class AtomicFormula(Formula):
    """Atomic formula (predicate)."""
    
    def __init__(self, predicate: Predicate):
        self.predicate = predicate
    
    def __repr__(self):
        return str(self.predicate)
    
    def variables(self) -> Set[Variable]:
        """Get all variables in formula."""
        variables = set()
        for arg in self.predicate.args:
            if isinstance(arg, Variable):
                variables.add(arg)
        return variables
    
    def substitute(self, substitution: Dict[Variable, Term]) -> 'AtomicFormula':
        """Apply substitution to formula."""
        new_args = []
        for arg in self.predicate.args:
            if isinstance(arg, Variable) and arg in substitution:
                new_args.append(substitution[arg])
            else:
                new_args.append(arg)
        return AtomicFormula(Predicate(self.predicate.name, new_args))


class CompoundFormula(Formula):
    """Compound formula with operator."""
    
    def __init__(self, operator: Operator, *operands: Formula):
        self.operator = operator
        self.operands = operands
    
    def __repr__(self):
        if self.operator == Operator.NOT:
            return f"{self.operator.value}{self.operands[0]}"
        elif self.operator in [Operator.UNIVERSAL, Operator.EXISTENTIAL]:
            return f"{self.operator.value}{self.operands[0]}"
        else:
            op_str = f" {self.operator.value} "
            return "(" + op_str.join(str(op) for op in self.operands) + ")"
    
    def variables(self) -> Set[Variable]:
        """Get all variables."""
        variables = set()
        for operand in self.operands:
            variables.update(operand.variables())
        return variables


class QuantifiedFormula(Formula):
    """Quantified formula."""
    
    def __init__(self, quantifier: Operator, variable: Variable, formula: Formula):
        if quantifier not in [Operator.UNIVERSAL, Operator.EXISTENTIAL]:
            raise ValueError("Invalid quantifier")
        
        self.quantifier = quantifier
        self.variable = variable
        self.formula = formula
    
    def __repr__(self):
        return f"{self.quantifier.value}{self.variable} {self.formula}"
    
    def variables(self) -> Set[Variable]:
        """Get free variables (not bound by quantifier)."""
        all_vars = self.formula.variables()
        all_vars.discard(self.variable)
        return all_vars


class Interpretation:
    """Interpretation of predicates over a domain."""
    
    def __init__(self, domain: Set[Constant], 
                 predicate_extensions: Dict[str, Set[Tuple[Constant, ...]]]):
        """
        Initialize interpretation.
        
        Args:
            domain: Domain of constants
            predicate_extensions: Maps predicate names to sets of tuples
        """
        self.domain = domain
        self.predicate_extensions = predicate_extensions
    
    def evaluate_predicate(self, predicate: Predicate) -> bool:
        """Evaluate a predicate under this interpretation."""
        if predicate.name not in self.predicate_extensions:
            return False
        
        # Convert arguments to constants
        args_tuple = tuple(arg for arg in predicate.args if isinstance(arg, Constant))
        
        if len(args_tuple) != len(predicate.args):
            return False  # Not all arguments are constants
        
        return args_tuple in self.predicate_extensions[predicate.name]
    
    def evaluate_formula(self, formula: Formula, 
                        assignment: Dict[Variable, Constant] = None) -> bool:
        """Evaluate formula under this interpretation."""
        if assignment is None:
            assignment = {}
        
        if isinstance(formula, AtomicFormula):
            # Substitute variables with their assignments
            substituted = formula.substitute(assignment)
            return self.evaluate_predicate(substituted.predicate)
        
        elif isinstance(formula, CompoundFormula):
            if formula.operator == Operator.NOT:
                return not self.evaluate_formula(formula.operands[0], assignment)
            
            elif formula.operator == Operator.AND:
                return all(self.evaluate_formula(op, assignment) for op in formula.operands)
            
            elif formula.operator == Operator.OR:
                return any(self.evaluate_formula(op, assignment) for op in formula.operands)
            
            elif formula.operator == Operator.IMPLIES:
                p = self.evaluate_formula(formula.operands[0], assignment)
                q = self.evaluate_formula(formula.operands[1], assignment)
                return (not p) or q
            
            elif formula.operator == Operator.IFF:
                p = self.evaluate_formula(formula.operands[0], assignment)
                q = self.evaluate_formula(formula.operands[1], assignment)
                return p == q
        
        elif isinstance(formula, QuantifiedFormula):
            if formula.quantifier == Operator.UNIVERSAL:
                # ∀X φ is true iff φ is true for all assignments to X
                for constant in self.domain:
                    new_assignment = assignment.copy()
                    new_assignment[formula.variable] = constant
                    if not self.evaluate_formula(formula.formula, new_assignment):
                        return False
                return True
            
            elif formula.quantifier == Operator.EXISTENTIAL:
                # ∃X φ is true iff φ is true for some assignment to X
                for constant in self.domain:
                    new_assignment = assignment.copy()
                    new_assignment[formula.variable] = constant
                    if self.evaluate_formula(formula.formula, new_assignment):
                        return True
                return False
        
        return False


class ModelChecker:
    """Checks if formulas are satisfied in interpretations."""
    
    @staticmethod
    def is_valid(formula: Formula, domain: Set[Constant], 
                 interpretations: List[Interpretation]) -> bool:
        """
        Check if formula is valid in all interpretations.
        
        Args:
            formula: Formula to check
            domain: Domain of discourse
            interpretations: List of interpretations to check
            
        Returns:
            True if valid in all interpretations
        """
        for interp in interpretations:
            if not interp.evaluate_formula(formula):
                return False
        return True
    
    @staticmethod
    def is_satisfiable(formula: Formula, interpretations: List[Interpretation]) -> bool:
        """Check if formula is satisfiable in at least one interpretation."""
        for interp in interpretations:
            if interp.evaluate_formula(formula):
                return True
        return False
    
    @staticmethod
    def is_tautology(formula: Formula, domain: Set[Constant],
                     interpretations: List[Interpretation]) -> bool:
        """Check if formula is a tautology."""
        return ModelChecker.is_valid(formula, domain, interpretations)
    
    @staticmethod
    def is_contradiction(formula: Formula, 
                        interpretations: List[Interpretation]) -> bool:
        """Check if formula is a contradiction."""
        for interp in interpretations:
            if interp.evaluate_formula(formula):
                return False
        return True


class PredicateLogicAnalyzer:
    """Analyzer for predicate logic properties."""
    
    @staticmethod
    def get_bound_variables(formula: Formula) -> Set[Variable]:
        """Get all bound variables in formula."""
        bound = set()
        
        if isinstance(formula, QuantifiedFormula):
            bound.add(formula.variable)
            bound.update(PredicateLogicAnalyzer.get_bound_variables(formula.formula))
        
        elif isinstance(formula, CompoundFormula):
            for operand in formula.operands:
                bound.update(PredicateLogicAnalyzer.get_bound_variables(operand))
        
        return bound
    
    @staticmethod
    def get_free_variables(formula: Formula) -> Set[Variable]:
        """Get all free (unbound) variables in formula."""
        all_vars = formula.variables() if hasattr(formula, 'variables') else set()
        bound_vars = PredicateLogicAnalyzer.get_bound_variables(formula)
        return all_vars - bound_vars
    
    @staticmethod
    def is_closed(formula: Formula) -> bool:
        """Check if formula is closed (no free variables)."""
        return len(PredicateLogicAnalyzer.get_free_variables(formula)) == 0
    
    @staticmethod
    def rename_variable(formula: Formula, old_var: Variable, 
                       new_var: Variable) -> Formula:
        """Rename a variable in a formula."""
        if isinstance(formula, AtomicFormula):
            new_args = []
            for arg in formula.predicate.args:
                if arg == old_var:
                    new_args.append(new_var)
                else:
                    new_args.append(arg)
            return AtomicFormula(Predicate(formula.predicate.name, new_args))
        
        elif isinstance(formula, CompoundFormula):
            new_operands = tuple(
                PredicateLogicAnalyzer.rename_variable(op, old_var, new_var)
                for op in formula.operands
            )
            return CompoundFormula(formula.operator, *new_operands)
        
        elif isinstance(formula, QuantifiedFormula):
            new_formula = PredicateLogicAnalyzer.rename_variable(
                formula.formula, old_var, new_var
            )
            if formula.variable == old_var:
                return QuantifiedFormula(formula.quantifier, new_var, new_formula)
            else:
                return QuantifiedFormula(formula.quantifier, formula.variable, new_formula)
        
        return formula


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("MODEL CHECKING AND SEMANTIC ANALYSIS")
    print("="*60)
    
    # Create domain
    domain = {Constant("Alice"), Constant("Bob"), Constant("Carol")}
    
    # Create interpretation
    predicate_extensions = {
        "Parent": {(Constant("Alice"), Constant("Bob")), 
                  (Constant("Carol"), Constant("Bob"))},
        "Female": {(Constant("Alice"),), (Constant("Carol"),)},
        "Male": {(Constant("Bob"),)}
    }
    
    interp = Interpretation(domain, predicate_extensions)
    
    print("\n1. Domain and Interpretation:")
    print("-" * 60)
    print(f"Domain: {domain}")
    print(f"Predicates: {list(predicate_extensions.keys())}")
    
    # Create formulas
    x = Variable("X")
    alice = Constant("Alice")
    
    # ∃X Female(X) - There exists a female
    exists_female = QuantifiedFormula(
        Operator.EXISTENTIAL,
        x,
        AtomicFormula(Predicate("Female", [x]))
    )
    
    print("\n2. Formula Evaluation:")
    print("-" * 60)
    print(f"Formula: {exists_female}")
    print(f"Evaluates to: {interp.evaluate_formula(exists_female)}")
    
    # ∀X Male(X) - Everyone is male
    all_male = QuantifiedFormula(
        Operator.UNIVERSAL,
        x,
        AtomicFormula(Predicate("Male", [x]))
    )
    
    print(f"\nFormula: {all_male}")
    print(f"Evaluates to: {interp.evaluate_formula(all_male)}")
    
    # Analysis
    print("\n3. Variable Analysis:")
    print("-" * 60)
    print(f"Free variables in {exists_female}: {PredicateLogicAnalyzer.get_free_variables(exists_female)}")
    print(f"Closed formula: {PredicateLogicAnalyzer.is_closed(exists_female)}")
