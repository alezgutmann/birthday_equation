#!/usr/bin/env python3
"""
Birthday Equation Generator

This script takes a date as input and generates arithmetic equations
using all possible combinations of operators between the digits.

Example: For date 09052005, it finds equations like (0+9+0-5) = 2*0+0+5
"""

import itertools
import re
from typing import List, Tuple, Optional


class BirthdayEquationGenerator:
    """Generator for arithmetic equations from date digits."""
    
    OPERATORS = ['+', '-', '*', '/']
    
    def __init__(self, date_string: str):
        """
        Initialize with a date string.
        
        Args:
            date_string: Date in format like "09052005" or "09/05/2005"
        """
        # Extract only digits from the input
        self.digits = [int(d) for d in re.findall(r'\d', date_string)]
        if len(self.digits) < 3:
            raise ValueError("Date must contain at least 3 digits")
        
        self.date_string = date_string
        print(f"Extracted digits: {self.digits}")
    
    def evaluate_expression(self, digits: List[int], operators: List[str]) -> Optional[float]:
        """
        Safely evaluate an arithmetic expression.
        
        Args:
            digits: List of digit values
            operators: List of operators between digits
            
        Returns:
            Result of evaluation or None if invalid (e.g., division by zero)
        """
        if len(operators) != len(digits) - 1:
            return None
            
        try:
            # Build the expression string
            expr = str(digits[0])
            for i, op in enumerate(operators):
                expr += f" {op} {digits[i + 1]}"
            
            # Evaluate the expression
            result = eval(expr)
            
            # Check for valid numeric result
            if isinstance(result, (int, float)) and not (isinstance(result, float) and 
                                                       (result != result or  # NaN check
                                                        abs(result) == float('inf'))):  # Infinity check
                return result
            return None
            
        except (ZeroDivisionError, OverflowError, ValueError):
            return None
    
    def format_expression(self, digits: List[int], operators: List[str]) -> str:
        """Format digits and operators into a readable expression string."""
        if len(operators) != len(digits) - 1:
            return ""
            
        expr = str(digits[0])
        for i, op in enumerate(operators):
            expr += f" {op} {digits[i + 1]}"
        return expr
    
    def generate_equations(self, tolerance: float = 1e-10) -> List[Tuple[str, str, float]]:
        """
        Generate all valid equations by trying different splits and operator combinations.
        
        Args:
            tolerance: Numerical tolerance for equality comparison
            
        Returns:
            List of tuples (left_expression, right_expression, value)
        """
        equations = []
        num_digits = len(self.digits)
        
        # Try different ways to split digits between left and right sides
        for split_point in range(1, num_digits):
            left_digits = self.digits[:split_point]
            right_digits = self.digits[split_point:]
            
            # Generate all operator combinations for left side
            if len(left_digits) > 1:
                left_operator_combinations = itertools.product(self.OPERATORS, repeat=len(left_digits)-1)
            else:
                left_operator_combinations = [[]]  # No operators needed for single digit
            
            # Generate all operator combinations for right side
            if len(right_digits) > 1:
                right_operator_combinations = itertools.product(self.OPERATORS, repeat=len(right_digits)-1)
            else:
                right_operator_combinations = [[]]  # No operators needed for single digit
            
            # Try all combinations
            for left_ops in left_operator_combinations:
                for right_ops in right_operator_combinations:
                    left_result = self.evaluate_expression(left_digits, list(left_ops))
                    right_result = self.evaluate_expression(right_digits, list(right_ops))
                    
                    # Check if both sides are valid and equal (within tolerance)
                    if (left_result is not None and right_result is not None and 
                        abs(left_result - right_result) <= tolerance):
                        
                        left_expr = self.format_expression(left_digits, list(left_ops))
                        right_expr = self.format_expression(right_digits, list(right_ops))
                        
                        equations.append((left_expr, right_expr, left_result))
        
        return equations
    
    def find_equations_with_grouping(self, tolerance: float = 1e-10) -> List[Tuple[str, str, float]]:
        """
        Find equations considering different groupings with parentheses.
        This is a more advanced version that considers operator precedence.
        """
        equations = []
        num_digits = len(self.digits)
        
        # Try different ways to split digits between left and right sides
        for split_point in range(1, num_digits):
            left_digits = self.digits[:split_point]
            right_digits = self.digits[split_point:]
            
            # For this implementation, we'll focus on the basic version
            # but add parentheses around each side for clarity
            if len(left_digits) > 1:
                left_operator_combinations = itertools.product(self.OPERATORS, repeat=len(left_digits)-1)
            else:
                left_operator_combinations = [[]]
            
            if len(right_digits) > 1:
                right_operator_combinations = itertools.product(self.OPERATORS, repeat=len(right_digits)-1)
            else:
                right_operator_combinations = [[]]
            
            for left_ops in left_operator_combinations:
                for right_ops in right_operator_combinations:
                    left_result = self.evaluate_expression(left_digits, list(left_ops))
                    right_result = self.evaluate_expression(right_digits, list(right_ops))
                    
                    if (left_result is not None and right_result is not None and 
                        abs(left_result - right_result) <= tolerance):
                        
                        # Add parentheses for multi-digit expressions
                        left_expr = self.format_expression(left_digits, list(left_ops))
                        right_expr = self.format_expression(right_digits, list(right_ops))
                        
                        if len(left_digits) > 1:
                            left_expr = f"({left_expr})"
                        if len(right_digits) > 1:
                            right_expr = f"({right_expr})"
                        
                        equations.append((left_expr, right_expr, left_result))
        
        return equations


def main():
    """Main function to run the birthday equation generator."""
    print("Birthday Equation Generator")
    print("=" * 40)
    
    while True:
        try:
            # Get user input
            date_input = input("\nEnter a date (e.g., 09052005, 09/05/2005) or 'quit' to exit: ").strip()
            
            if date_input.lower() in ['quit', 'q', 'exit']:
                print("Goodbye!")
                break
            
            if not date_input:
                print("Please enter a valid date.")
                continue
            
            # Create generator and find equations
            generator = BirthdayEquationGenerator(date_input)
            
            print(f"\nSearching for equations using digits: {generator.digits}")
            print("This may take a moment for dates with many digits...")
            
            # Generate basic equations
            equations = generator.generate_equations()
            
            if equations:
                print(f"\nFound {len(equations)} valid equations:")
                print("-" * 40)
                
                # Remove duplicates and sort by value
                unique_equations = list(set(equations))
                unique_equations.sort(key=lambda x: x[2])  # Sort by result value
                
                # Display equations (limit to first 20 to avoid overwhelming output)
                display_limit = 20
                for i, (left, right, value) in enumerate(unique_equations[:display_limit]):
                    print(f"{i+1:2d}. {left} = {right}  (= {value})")
                
                if len(unique_equations) > display_limit:
                    print(f"... and {len(unique_equations) - display_limit} more equations")
                
                # Also try with grouping/parentheses
                print(f"\nWith parentheses grouping:")
                print("-" * 40)
                grouped_equations = generator.find_equations_with_grouping()
                unique_grouped = list(set(grouped_equations))
                unique_grouped.sort(key=lambda x: x[2])
                
                for i, (left, right, value) in enumerate(unique_grouped[:display_limit]):
                    print(f"{i+1:2d}. {left} = {right}  (= {value})")
                
                if len(unique_grouped) > display_limit:
                    print(f"... and {len(unique_grouped) - display_limit} more equations")
            else:
                print("\nNo valid equations found for this date.")
                print("Try a different date or one with more digits.")
        
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()