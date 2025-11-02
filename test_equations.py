#!/usr/bin/env python3
"""
Test script for the birthday equation generators.
"""

from birthday_equation import BirthdayEquationGenerator
from advanced_birthday_equation import AdvancedBirthdayEquationGenerator


def test_basic_functionality():
    """Test basic functionality with simple examples."""
    print("Testing Basic Birthday Equation Generator")
    print("=" * 50)
    
    test_cases = [
        "123",      # Simple 3-digit case
        "1234",     # 4-digit case  
        "09052005", # The example from the prompt
        "12345"     # 5-digit case
    ]
    
    for test_date in test_cases:
        print(f"\nTesting with: {test_date}")
        try:
            generator = BirthdayEquationGenerator(test_date)
            equations = generator.generate_equations()
            
            if equations:
                print(f"Found {len(equations)} equations")
                # Show first few
                unique_eqs = list(set(equations))[:3]
                for left, right, val in unique_eqs:
                    print(f"  {left} = {right} (= {val})")
            else:
                print("  No equations found")
                
        except Exception as e:
            print(f"  Error: {e}")


def test_advanced_functionality():
    """Test the advanced generator."""
    print(f"\n\nTesting Advanced Birthday Equation Generator")
    print("=" * 50)
    
    test_cases = ["123", "09052005"]
    
    for test_date in test_cases:
        print(f"\nTesting with: {test_date}")
        try:
            generator = AdvancedBirthdayEquationGenerator(test_date)
            equations = generator.find_matching_equations()
            
            if equations:
                print(f"Found {len(equations)} equations")
                unique_eqs = list(set(equations))[:3]
                for left, right, val in unique_eqs:
                    print(f"  {left} = {right} (= {val})")
            else:
                print("  No equations found")
                
        except Exception as e:
            print(f"  Error: {e}")


def manual_verification():
    """Manually verify the example from the prompt."""
    print(f"\n\nManual Verification of Example")
    print("=" * 50)
    
    # For 09052005, let's manually check if (0+9+0-5) = 2*0+0+5 works
    left_side = 0 + 9 + 0 - 5  # Should be 4
    right_side = 2 * 0 + 0 + 5  # Should be 5
    
    print(f"Manual calculation of example:")
    print(f"Left side (0+9+0-5) = {left_side}")
    print(f"Right side (2*0+0+5) = {right_side}")
    print(f"Equal? {left_side == right_side}")
    
    # Let's try to find a working version
    print(f"\nLet's find equations that actually work for 09052005:")
    
    # Digits: [0, 9, 0, 5, 2, 0, 0, 5]
    digits = [0, 9, 0, 5, 2, 0, 0, 5]
    
    # Try some simple splits and operations
    # Split 1: [0, 9] and [0, 5, 2, 0, 0, 5]
    left1 = 0 + 9  # = 9
    right1 = 0 + 5 + 2 + 0 + 0 + 5  # = 12
    print(f"0 + 9 = {left1}, 0 + 5 + 2 + 0 + 0 + 5 = {right1} (Equal: {left1 == right1})")
    
    # Split 2: [0, 9, 0] and [5, 2, 0, 0, 5]  
    left2 = 0 + 9 - 0  # = 9
    right2 = 5 + 2 - 0 - 0 - 5  # = 2
    print(f"0 + 9 - 0 = {left2}, 5 + 2 - 0 - 0 - 5 = {right2} (Equal: {left2 == right2})")
    
    # Try multiplication/division
    left3 = 0 * 9 + 0  # = 0
    right3 = 5 - 2 - 0 - 0 - 5  # = -2
    print(f"0 * 9 + 0 = {left3}, 5 - 2 - 0 - 0 - 5 = {right3} (Equal: {left3 == right3})")


if __name__ == "__main__":
    test_basic_functionality()
    test_advanced_functionality() 
    manual_verification()