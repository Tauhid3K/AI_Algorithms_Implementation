def take(medicine, count, actual_med, actual_count):
    """
    Predicate: Take(medicine, count)
    Returns True if the medicine and count match the actual action taken.
    """
    return medicine == actual_med and count == actual_count

def check_prescription(actual_med, actual_count):
    # Logic: Take(Advil, 2) OR Take(Tylenol, 3)
    option1 = take("Advil", 2, actual_med, actual_count)
    option2 = take("Tylenol", 3, actual_med, actual_count)
    
    result = option1 or option2
    
    print(f"Action: Took {actual_count} {actual_med}")
    print(f"Compliance: {'Correct' if result else 'Incorrect'}\n")

if __name__ == "__main__":
    print("--- Predicate Logic Check: 'Take 2 Advil OR 3 Tylenol' ---\n")
    
    # Test cases
    check_prescription("Advil", 2)    # Matches Option 1
    check_prescription("Tylenol", 3)  # Matches Option 2
    check_prescription("Advil", 3)    # Wrong amount
    check_prescription("Aspirin", 2)  # Wrong medicine
