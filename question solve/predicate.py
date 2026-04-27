def solve_predicate_question_c():
    """
    c) Take either 2 Advil or 3 Tylenol

    Predicate logic form:
    Take(Advil, 2) OR Take(Tylenol, 3)
    """

    print("\nQuestion c: Take either 2 Advil or 3 Tylenol")
    print("Predicate form: Take(Advil, 2) OR Take(Tylenol, 3)")

    rows = [
        (True, False),
        (False, True),
        (True, True),
        (False, False),
    ]

    print("\nTake(Advil,2) | Take(Tylenol,3) | Result")
    print("------------------------------------------")
    for advil_2, tylenol_3 in rows:
        result = advil_2 or tylenol_3
        print(f"{'T' if advil_2 else 'F'}             | {'T' if tylenol_3 else 'F'}               | {'T' if result else 'F'}")


if __name__ == "__main__":
    solve_predicate_question_c()
