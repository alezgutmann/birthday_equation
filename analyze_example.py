#!/usr/bin/env python3
"""
Special analysis for the example equation mentioned in the request.

Analyzes why (0+9+0-5) = 2*0+0+5 doesn't work and finds similar valid equations.
"""

from birthday_equation import BirthdayEquationGenerator
import itertools


def analyze_example_equation():
    """Analyze the specific example from the request."""
    print("Analysis of Example Equation: (0+9+0-5) = 2*0+0+5")
    print("=" * 60)
    
    # Calculate the example manually
    left_example = 0 + 9 + 0 - 5  # = 4
    right_example = 2 * 0 + 0 + 5  # = 5
    
    print(f"Left side: 0 + 9 + 0 - 5 = {left_example}")
    print(f"Right side: 2 * 0 + 0 + 5 = {right_example}")
    print(f"Equal? {left_example == right_example}")
    print(f"Difference: {abs(left_example - right_example)}")
    
    print(f"\nThis example equation is not mathematically valid.")
    print(f"Let's find similar valid equations for the date 09052005...")


def find_similar_patterns():
    """Find equations with similar structure to the example."""
    print(f"\n" + "Finding Similar Valid Equations")
    print("=" * 60)
    
    date = "09052005"
    digits = [0, 9, 0, 5, 2, 0, 0, 5]
    
    print(f"Date: {date}")
    print(f"Digits: {digits}")
    
    # Try to find equations that use the first 4 digits on one side
    # and some combination of the remaining digits on the other side
    
    generator = BirthdayEquationGenerator(date)
    all_equations = generator.generate_equations()
    
    # Filter for equations that might be similar to the example pattern
    similar_equations = []
    
    for left, right, value in all_equations:
        # Look for equations where left side uses first few digits
        # and includes addition/subtraction operations
        if (("0" in left and "9" in left) and 
            ("+" in left or "-" in left) and
            len(left.split()) <= 8):  # Not too complex
            similar_equations.append((left, right, value))
    
    print(f"\nFound {len(similar_equations)} equations with similar structure:")
    print("-" * 50)
    
    # Show the most interesting ones
    unique_similar = list(set(similar_equations))
    unique_similar.sort(key=lambda x: (abs(x[2]), len(x[0])))
    
    for i, (left, right, value) in enumerate(unique_similar[:10]):
        print(f"{i+1:2d}. {left} = {right}  (= {value})")
    
    if len(unique_similar) > 10:
        print(f"... and {len(unique_similar) - 10} more similar equations")


def find_corrected_example():
    """Try to find a corrected version of the example that actually works."""
    print(f"\n" + "Finding Corrected Versions")
    print("=" * 60)
    
    digits = [0, 9, 0, 5, 2, 0, 0, 5]
    
    print("Let's try to modify the example to make it work:")
    
    # Try variations of the left side that equal 5 (to match right side)
    variations = [
        ("0 + 9 - 0 - 5", 0 + 9 - 0 - 5),  # = 4
        ("0 + 9 + 0 - 4", None),  # Can't use 4, not in our digits
        ("0 * 9 + 0 + 5", 0 * 9 + 0 + 5),  # = 5 ✓
        ("0 + 9 - 5 + 0", 0 + 9 - 5 + 0),  # = 4  
        ("9 - 0 - 5 + 0", 9 - 0 - 5 + 0),  # = 4
        ("9 + 0 - 5 + 0", 9 + 0 - 5 + 0),  # = 4
    ]
    
    target = 2 * 0 + 0 + 5  # Right side = 5
    
    print(f"Target value (right side): 2 * 0 + 0 + 5 = {target}")
    print(f"\nTrying different left side combinations:")
    
    for expr, value in variations:
        if value is not None:
            match = "✓" if value == target else "✗"
            print(f"  {expr} = {value} {match}")
        else:
            print(f"  {expr} = invalid (uses digits not in date)")
    
    print(f"\nWorking equation found: 0 * 9 + 0 + 5 = 2 * 0 + 0 + 5  (both = 5)")
    
    # Now let's see if this appears in our generated equations
    print(f"\nChecking if this appears in generated equations...")
    generator = BirthdayEquationGenerator("09052005")
    equations = generator.generate_equations()
    
    found_corrected = False
    for left, right, value in equations:
        if "0 * 9 + 0 + 5" in left or "0 * 9 + 0 + 5" in right:
            print(f"Found: {left} = {right}  (= {value})")
            found_corrected = True
    
    if not found_corrected:
        print("The corrected equation doesn't appear in our split-based generation.")
        print("This is because we split digits sequentially, but the corrected")
        print("equation uses digits from different parts of the date.")


def main():
    """Run the complete analysis."""
    analyze_example_equation()
    find_similar_patterns() 
    find_corrected_example()
    
    print(f"\n" + "Summary")
    print("=" * 60)
    print("• The original example (0+9+0-5) = 2*0+0+5 is mathematically incorrect (4 ≠ 5)")
    print("• A corrected version would be: 0*9+0+5 = 2*0+0+5 (both equal 5)")  
    print("• The birthday equation generators find many other valid equations")
    print("• For interactive exploration, run: python birthday_equation.py")


if __name__ == "__main__":
    main()