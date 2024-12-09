def calculate_baseline(numbers):
    if not numbers:
        return None
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements in the list must be numbers.")

    return sum(numbers) / len(numbers)