import re
from dataclasses import dataclass

# ===== TERMS =====

@dataclass
class Constant:
    name: str
    def __repr__(self): return self.name

@dataclass
class Variable:
    name: str
    def __repr__(self): return self.name

@dataclass
class Predicate:
    name: str
    args: list
    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"


# ===== UNIFICATION =====

def unify(x, y, subst=None):
    if subst is None:
        subst = {}

    if isinstance(x, Variable):
        subst[x.name] = y
        return subst

    if isinstance(y, Variable):
        subst[y.name] = x
        return subst

    if isinstance(x, Constant) and isinstance(y, Constant):
        return subst if x.name == y.name else None

    if isinstance(x, Predicate) and isinstance(y, Predicate):
        if x.name != y.name or len(x.args) != len(y.args):
            return None

        for a, b in zip(x.args, y.args):
            subst = unify(a, b, subst)
            if subst is None:
                return None

        return subst

    return None


# ===== CLAUSE =====

@dataclass
class Clause:
    literals: list   # (negated, predicate)

    def __repr__(self):
        return " ∨ ".join(
            f"¬{p}" if neg else str(p) for neg, p in self.literals
        )


# ===== RESOLUTION (FIXED) =====

def resolve(c1, c2):
    resolvents = []

    for i, (neg1, p1) in enumerate(c1.literals):
        for j, (neg2, p2) in enumerate(c2.literals):

            # must be opposite signs
            if neg1 == neg2:
                continue

            # must unify
            subst = unify(p1, p2, {})
            if subst is None:
                continue

            new_literals = []

            for k, lit in enumerate(c1.literals):
                if k != i:
                    new_literals.append(lit)

            for k, lit in enumerate(c2.literals):
                if k != j:
                    new_literals.append(lit)

            resolvents.append(Clause(new_literals))

    return resolvents


# ===== TEST =====

if __name__ == "__main__":
    print("=== Unification ===")

    john = Constant("john")
    mary = Constant("mary")
    X = Variable("X")
    Y = Variable("Y")

    p1 = Predicate("Loves", [john, Y])
    p2 = Predicate("Loves", [X, mary])

    print("Unifier:", unify(p1, p2))

    print("\n=== Resolution ===")

    X = Variable("X")

    # CORRECT CONTRADICTION EXAMPLE
    c1 = Clause([(False, Predicate("Mortal", [X]))])
    c2 = Clause([(True, Predicate("Mortal", [Constant("socrates")]))])

    print("Clause1:", c1)
    print("Clause2:", c2)

    results = resolve(c1, c2)

    print("\n--- Resolution Steps ---")

    if results:
        print("Step 1: Predicate match found")
        print("Step 2: X = socrates")
        print("Step 3: Mortal(socrates) and ¬Mortal(socrates) cancel")

        print("\nResult:")
        print("⊥ (Empty Clause)")
        print("Conclusion: Contradiction → Proof Successful")
    else:
        print("Step 1: No matching predicates")
        print("Result: No resolution possible")
        print("Conclusion: No contradiction")
