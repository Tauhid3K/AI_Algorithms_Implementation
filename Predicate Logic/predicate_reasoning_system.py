class PredicateLogic:
    def __init__(self, U):
        self.U = U
        self.P = {}

    def add(self, name, values):
        self.P[name] = set(values)

    def eval(self, name, args):
        return tuple(args) in self.P.get(name, set())

    # ∀x P(x)
    def forall(self, name):
        print(f"\n∀x {name}(x)")
        for x in self.U:
            print(f"  {name}({x}): {self.eval(name, [x])}")
        return all(self.eval(name, [x]) for x in self.U)

    # ∃x P(x)
    def exists(self, name):
        print(f"\n∃x {name}(x)")
        for x in self.U:
            print(f"  {name}({x}): {self.eval(name, [x])}")
        return any(self.eval(name, [x]) for x in self.U)

    # ∃x,y P(x,y) #for pairs 
    def exists2(self, name):
        print(f"\n∃x,y {name}(x,y)")
        found = False

        for x in self.U:
            for y in self.U:
                if self.eval(name, [x, y]):
                    print(f"  {name}({x},{y}): True")
                    found = True

        return found


    # relation check
    def relation(self, name, a, b):
        print(f"\n{name}({a}, {b}) → {self.eval(name, [a, b])}")

    def model(self):
        print("\nModel Checking")
        print("Universe:", self.U)
        print("Predicates:", list(self.P.keys()))


# =========================
# 🔥 EXAMPLES
# =========================

U = ["Alice", "Bob", "Charlie", "Diana"]
logic = PredicateLogic(U)

print("\n>>> EXAMPLE 1: Universe & Predicates")
logic.add("Parent", [("Alice","Bob"), ("Alice","Charlie"), ("Bob","Diana")])
logic.add("Person", [("Alice",), ("Bob",), ("Charlie",), ("Diana",)])

print("✓ Universe:", set(U))
print("✓ Parent/2: 3 tuples")
print("✓ Person/1: 4 tuples")

print("\n>>> EXAMPLE 2: ∀x Person(x)")
print("Result:", logic.forall("Person"))

print("\n>>> EXAMPLE 3: ∃x,y Parent(x,y)")
print("Result:", logic.exists2("Parent"))

print("\n>>> EXAMPLE 4: De Morgan Law")
print("¬∀x P(x) ≡ ∃x ¬P(x)")

print("\n>>> EXAMPLE 5: Relation Check")
logic.relation("Parent", "Alice", "Bob")
logic.relation("Parent", "Charlie", "Diana")

print("\n>>> EXAMPLE 6: Model")
logic.add("Married", [("Alice","Tom"), ("Bob","Jane")])
print("✓ Married/2 added")

logic.model()
