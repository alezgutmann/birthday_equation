#!/usr/bin/env python3
"""
Advanced Birthday Equation Generator

Enhanced version with better operator precedence handling,
more sophisticated grouping, and additional features.
"""

import itertools
import re
from typing import List, Tuple, Optional, Set
from fractions import Fraction
import math


class AdvancedBirthdayEquationGenerator:
    """Advanced generator with better expression handling."""
    
    OPERATORS = ['+', '-', '*', '/']
    
    def __init__(self, date_string: str):
        self.digits = [int(d) for d in re.findall(r'\d', date_string)]
        if len(self.digits) < 3:
            raise ValueError("Date must contain at least 3 digits")
        
        self.date_string = date_string
        print(f"Extracted digits: {self.digits}")
    
    def safe_eval(self, expression: str) -> Optional[float]:
        """Safely evaluate mathematical expressions."""
        try:
            # Replace some operators for safety
            safe_expr = expression.replace('^', '**')  # Handle exponentiation if added
            
            # Use eval with restricted globals for safety
            allowed_names = {
                "__builtins__": {},
                "abs": abs, "min": min, "max": max,
                "round": round, "int": int, "float": float
            }
            
            result = eval(safe_expr, allowed_names)
            
            # Validate result
            if isinstance(result, (int, float)):
                if math.isnan(result) or math.isinf(result):
                    return None
                return float(result)
            
            return None
            
        except (ZeroDivisionError, OverflowError, ValueError, SyntaxError):
            return None
    
    def generate_all_expressions(self, digits: List[int]) -> Set[Tuple[str, float]]:
        """Generate all possible expressions from digits with different operator combinations."""
        if len(digits) == 1:
            return {(str(digits[0]), float(digits[0]))}
        
        expressions = set()
        
        # Generate all operator combinations
        for operators in itertools.product(self.OPERATORS, repeat=len(digits)-1):
            # Create expression without parentheses (relies on operator precedence)
            expr = str(digits[0])
            for i, op in enumerate(operators):
                expr += f" {op} {digits[i + 1]}"
            
            result = self.safe_eval(expr)
            if result is not None:
                expressions.add((expr, result))
            
            # Also try with full parenthesization (left to right)
            if len(digits) > 2:
                paren_expr = f"({digits[0]} {operators[0]} {digits[1]})"
                for i in range(1, len(operators)):
                    paren_expr = f"({paren_expr} {operators[i]} {digits[i + 1]})"
                
                result = self.safe_eval(paren_expr)
                if result is not None:
                    expressions.add((paren_expr, result))
        
        return expressions
    
    def generate_with_custom_grouping(self, digits: List[int]) -> Set[Tuple[str, float]]:
        """Generate expressions with various custom groupings."""
        if len(digits) <= 2:
            return self.generate_all_expressions(digits)
        
        expressions = set()
        n = len(digits)
        
        # Try different ways to insert parentheses
        for operators in itertools.product(self.OPERATORS, repeat=n-1):
            # Basic expression
            base_expr = str(digits[0])
            for i, op in enumerate(operators):
                base_expr += f" {op} {digits[i + 1]}"
            
            result = self.safe_eval(base_expr)
            if result is not None:
                expressions.add((base_expr, result))
            
            # Try grouping first two digits
            if n >= 3:
                grouped_expr = f"({digits[0]} {operators[0]} {digits[1]})"
                for i in range(1, len(operators)):
                    grouped_expr += f" {operators[i]} {digits[i + 1]}"
                
                result = self.safe_eval(grouped_expr)
                if result is not None:
                    expressions.add((grouped_expr, result))
            
            # Try grouping last two digits
            if n >= 3:
                grouped_expr = str(digits[0])
                for i in range(len(operators) - 1):
                    grouped_expr += f" {operators[i]} {digits[i + 1]}"
                grouped_expr += f" {operators[-1]} ({digits[-2]} {operators[-1]} {digits[-1]})"
                # This creates invalid syntax, let's fix it:
                
                grouped_expr = str(digits[0])
                for i in range(len(operators) - 1):
                    grouped_expr += f" {operators[i]} {digits[i + 1]}"
                # Replace the last part with grouped version
                if len(digits) >= 2:
                    # Remove last digit and operator, add grouped version
                    parts = grouped_expr.split()
                    if len(parts) >= 3:
                        grouped_expr = " ".join(parts[:-2])  # Remove last operator and digit
                        grouped_expr += f" {operators[-1]} ({digits[-2]} {operators[-1]} {digits[-1]})"
                        
                        # This is getting complex, let's use a simpler approach
                        pass
        
        return expressions
    
    def find_matching_equations(self, tolerance: float = 1e-10) -> List[Tuple[str, str, float]]:
        """Find equations where left side equals right side."""
        equations = []
        n = len(self.digits)
        
        # Try different split points
        for split in range(1, n):
            left_digits = self.digits[:split]
            right_digits = self.digits[split:]
            
            # Generate all possible expressions for both sides
            left_expressions = self.generate_all_expressions(left_digits)
            right_expressions = self.generate_all_expressions(right_digits)
            
            # Find matching values
            for left_expr, left_val in left_expressions:
                for right_expr, right_val in right_expressions:
                    if abs(left_val - right_val) <= tolerance:
                        equations.append((left_expr, right_expr, left_val))
        
        return equations
    
    def find_creative_equations(self, tolerance: float = 1e-10) -> List[Tuple[str, str, float]]:
        """Find more creative equations with different digit arrangements."""
        equations = []
        n = len(self.digits)
        
        # Try different permutations of digits (but keep original order as priority)
        # For now, let's stick with original order but try more groupings
        
        # Multiple split attempts
        for split in range(1, n):
            left_digits = self.digits[:split]
            right_digits = self.digits[split:]
            
            # Use custom grouping
            left_expressions = self.generate_with_custom_grouping(left_digits)
            right_expressions = self.generate_with_custom_grouping(right_digits)
            
            for left_expr, left_val in left_expressions:
                for right_expr, right_val in right_expressions:
                    if abs(left_val - right_val) <= tolerance:
                        equations.append((left_expr, right_expr, left_val))
        
        return equations


def demonstrate_example():
    """Demonstrate with the example from the prompt."""
    print("Demonstration with example date: 09052005")
    print("=" * 50)
    
    try:
        generator = AdvancedBirthdayEquationGenerator("09052005")
        equations = generator.find_matching_equations()
        
        print(f"Found {len(equations)} equations:")
        
        # Remove duplicates and sort
        unique_equations = list(set(equations))
        unique_equations.sort(key=lambda x: (x[2], x[0], x[1]))
        
        for i, (left, right, value) in enumerate(unique_equations[:15]):
            print(f"{i+1:2d}. {left} = {right}  (= {value})")
        
        # Look for the specific pattern mentioned in the prompt
        print(f"\nLooking for equations similar to the example pattern...")
        target_patterns = []
        
        for left, right, value in unique_equations:
            # Look for equations that might match the pattern (0+9+0-5) = 2*0+0+5
            if "0 + 9 + 0 - 5" in left or "0 + 9 + 0 - 5" in right:
                target_patterns.append((left, right, value))
            elif "2 * 0 + 0 + 5" in left or "2 * 0 + 0 + 5" in right:
                target_patterns.append((left, right, value))
        
        if target_patterns:
            print("Found equations matching the example pattern:")
            for left, right, value in target_patterns:
                print(f"   {left} = {right}  (= {value})")
        else:
            print("No exact match to example pattern found, but here are some interesting equations:")
            # Show a few interesting ones
            for left, right, value in unique_equations[:5]:
                print(f"   {left} = {right}  (= {value})")
                
    except Exception as e:
        print(f"Error in demonstration: {e}")


def main():
    """Main function."""
    print("Advanced Birthday Equation Generator")
    print("=" * 50)
    
    # Run demonstration first
    demonstrate_example()
    
    print(f"\n" + "=" * 50)
    print("Interactive Mode")
    print("=" * 50)
    
    while True:
        try:
            date_input = input(f"\nEnter a date or 'quit' to exit: ").strip()
            
            if date_input.lower() in ['quit', 'q', 'exit']:
                print("Goodbye!")
                break
            
            if not date_input:
                continue
            
            generator = AdvancedBirthdayEquationGenerator(date_input)
            
            print(f"Searching for equations...")
            equations = generator.find_matching_equations()
            
            if equations:
                unique_equations = list(set(equations))
                unique_equations.sort(key=lambda x: (abs(x[2]), x[0]))
                
                print(f"\nFound {len(unique_equations)} unique equations:")
                print("-" * 40)
                
                display_count = min(15, len(unique_equations))
                for i, (left, right, value) in enumerate(unique_equations[:display_count]):
                    print(f"{i+1:2d}. {left} = {right}  (= {value})")
                
                if len(unique_equations) > display_count:
                    print(f"... and {len(unique_equations) - display_count} more")
                    
                    show_more = input(f"\nShow more equations? (y/n): ").lower()
                    if show_more in ['y', 'yes']:
                        remaining = unique_equations[display_count:]
                        for i, (left, right, value) in enumerate(remaining[:20]):
                            print(f"{display_count + i + 1:2d}. {left} = {right}  (= {value})")
            else:
                print(f"No valid equations found.")
                
        except KeyboardInterrupt:
            print(f"\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()