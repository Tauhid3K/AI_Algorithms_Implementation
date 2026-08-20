def solve_predicate_logic(): 
    
    socrates = "Socrates"
    is_human = {socrates: True}
    mortal_status = {}
    
    rule_a = f"If Human(x) -> Mortal(x), then Human({socrates}) -> Mortal({socrates})"
    print(f"Universal Instantiation: {rule_a}")
    
    print()

    if is_human.get(socrates):
        mortal_status[socrates] = True

    if mortal_status.get(socrates):
        print("We found a mortal (Socrates), so we can say Existential Mortal(x).")

    print()

solve_predicate_logic()
