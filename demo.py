#!/usr/bin/env python3
"""
Quick demo of the birthday equation generator.
"""

from birthday_equation import BirthdayEquationGenerator


def quick_demo():
    """Run a quick demonstration with several examples."""
    
    print("Birthday Equation Generator - Quick Demo")
    print("=" * 50)
    
    examples = [
        ("123", "Simple 3-digit example"),
        ("1111", "All same digits"),
        ("2024", "Current year"),
        ("09052005", "The original example"),
        ("31121999", "Another birthday format")
    ]
    
    for date_str, description in examples:
        print(f"\n{description}: {date_str}")
        print("-" * 30)
        
        try:
            generator = BirthdayEquationGenerator(date_str)
            equations = generator.generate_equations()
            
            if equations:
                # Remove duplicates and show first few
                unique_equations = list(set(equations))
                unique_equations.sort(key=lambda x: (abs(x[2]), len(x[0])))  # Sort by value magnitude, then expression length
                
                count_to_show = min(5, len(unique_equations))
                print(f"Found {len(unique_equations)} unique equations. Showing first {count_to_show}:")
                
                for i, (left, right, value) in enumerate(unique_equations[:count_to_show]):
                    print(f"  {i+1}. {left} = {right}  (= {value})")
                    
                if len(unique_equations) > count_to_show:
                    print(f"  ... and {len(unique_equations) - count_to_show} more!")
                    
            else:
                print("  No valid equations found for this date.")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\n" + "=" * 50)
    print("Demo completed! Try running the main scripts for interactive mode:")
    print("  python birthday_equation.py")
    print("  python advanced_birthday_equation.py")


if __name__ == "__main__":
    quick_demo()