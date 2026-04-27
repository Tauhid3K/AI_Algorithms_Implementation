"""
Logic Implementation
Implements basic logic gates and Boolean operations.
"""

from typing import List, Dict, Tuple #discribes data types
import re                            #for pattern matching and manipulation


# =========================
# Logic Gates
# =========================

class LogicGate:
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, *inputs: bool) -> bool:  
        raise NotImplementedError
#every gate must define its own evaluate method (own logic)

class ANDGate(LogicGate):
    def __init__(self):
        super().__init__("AND")

    def evaluate(self, *inputs: bool) -> bool:
        return all(inputs)


class ORGate(LogicGate):
    def __init__(self):
        super().__init__("OR")

    def evaluate(self, *inputs: bool) -> bool:
        return any(inputs)


class NOTGate(LogicGate):
    def __init__(self):
        super().__init__("NOT")

    def evaluate(self, *inputs: bool) -> bool:
        if len(inputs) != 1:
            raise ValueError("NOT gate requires exactly one input")
        return not inputs[0]


class XORGate(LogicGate):
    def __init__(self):
        super().__init__("XOR")

    def evaluate(self, *inputs: bool) -> bool:
        if len(inputs) != 2:
            raise ValueError("XOR gate requires exactly two inputs")
        return inputs[0] != inputs[1]


# =========================
# Boolean Expression
# =========================

class BooleanExpression:
    def __init__(self, expression: str):
        self.expression = expression
        self.variables = self._extract_variables()

    def _extract_variables(self) -> set:
        # ✅ FIX: only single-letter variables (A, B, C)
        return set(re.findall(r'\b[A-Z]\b', self.expression))

    def evaluate(self, **variable_values: bool) -> bool:
        expr = self.expression

        # ✅ Safe variable replacement
        for var in self.variables:
            if var not in variable_values:
                raise ValueError(f"Missing value for variable {var}")

            expr = re.sub(rf'\b{var}\b', str(variable_values[var]), expr)

        # Replace operators
        expr = expr.replace("AND", "and")
        expr = expr.replace("OR", "or")
        expr = expr.replace("NOT", "not")
        expr = expr.replace("^", "and")
        expr = expr.replace("|", "or")
        expr = expr.replace("~", "not ")

        # ✅ Safe eval
        return bool(eval(expr, {"__builtins__": None}, {}))

    def truth_table(self) -> List[Dict]:
        from itertools import product

        table = []
        vars_sorted = sorted(self.variables)

        for values in product([False, True], repeat=len(vars_sorted)):
            var_dict = dict(zip(vars_sorted, values))
            result = self.evaluate(**var_dict)
            row = {**var_dict, "Result": result}
            table.append(row)

        return table

    def print_truth_table(self):
        table = self.truth_table()

        if not table:
            return

        columns = sorted(self.variables) + ["Result"]

        width = 6  # column width

        # Header
        header = " | ".join(f"{col:^{width}}" for col in columns)
        print(header)
        print("-" * len(header))

        # Rows (0/1 output)
        for row in table:
            values = [str(int(row[col])) for col in columns]
            print(" | ".join(f"{v:^{width}}" for v in values))


# =========================
# Analyzer
# =========================

class TruthTableAnalyzer:

    @staticmethod
    def is_tautology(expression: BooleanExpression) -> bool:
        return all(row["Result"] for row in expression.truth_table())

    @staticmethod
    def is_contradiction(expression: BooleanExpression) -> bool:
        return not any(row["Result"] for row in expression.truth_table())

    @staticmethod
    def is_contingency(expression: BooleanExpression) -> bool:
        return not (
            TruthTableAnalyzer.is_tautology(expression) or
            TruthTableAnalyzer.is_contradiction(expression)
        )

    @staticmethod
    def are_equivalent(expr1: BooleanExpression, expr2: BooleanExpression) -> bool:
        from itertools import product

        all_vars = sorted(expr1.variables | expr2.variables)

        for values in product([False, True], repeat=len(all_vars)):
            var_dict = dict(zip(all_vars, values))

            r1 = expr1.evaluate(**{v: var_dict[v] for v in expr1.variables})
            r2 = expr2.evaluate(**{v: var_dict[v] for v in expr2.variables})

            if r1 != r2:
                return False

        return True

    @staticmethod
    def demorgan_first_law(a: bool, b: bool) -> Tuple[bool, bool]:
        return not (a and b), (not a) or (not b)

    @staticmethod
    def demorgan_second_law(a: bool, b: bool) -> Tuple[bool, bool]:
        return not (a or b), (not a) and (not b)


# =========================
# MAIN TEST
# =========================

if __name__ == "__main__":
    print("=== Logic Gates ===")

    and_gate = ANDGate()
    or_gate = ORGate()
    not_gate = NOTGate()
    xor_gate = XORGate()

    print("AND(True, True) =", int(and_gate.evaluate(True, True)))
    print("AND(True, False) =", int(and_gate.evaluate(True, False)))
    print("OR(True, False) =", int(or_gate.evaluate(True, False)))
    print("NOT(True) =", int(not_gate.evaluate(True)))
    print("XOR(True, False) =", int(xor_gate.evaluate(True, False)))

    print("\n=== Boolean Expression ===")

    expr = BooleanExpression("A AND B OR NOT C")
    print("\nExpression: A AND B OR NOT C")
    expr.print_truth_table()

    print("\n=== Truth Table Analysis ===")

    tautology_expr = BooleanExpression("A OR NOT A")
    print(f"\n'{tautology_expr.expression}' is tautology:",
          int(TruthTableAnalyzer.is_tautology(tautology_expr)))

    contradiction_expr = BooleanExpression("A AND NOT A")
    print(f"'{contradiction_expr.expression}' is contradiction:",
          int(TruthTableAnalyzer.is_contradiction(contradiction_expr)))

    expr1 = BooleanExpression("A OR B")
    expr2 = BooleanExpression("B OR A")
    print(f"\n'{expr1.expression}' equivalent to '{expr2.expression}':",
          int(TruthTableAnalyzer.are_equivalent(expr1, expr2)))
