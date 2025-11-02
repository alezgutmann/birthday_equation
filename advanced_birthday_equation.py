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
    
    # Include '^' for power and 'root' for n-th root; factorial will be available via tokenization
    OPERATORS = ['+', '-', '*', '/', '^', 'root']
    
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
            # We'll map '^' to '**' in the eval step but also provide fact/root functions
            safe_expr = expression.replace('^', '**')

            def fact(n):
                try:
                    ni = int(n)
                except Exception:
                    raise ValueError("factorial requires integer")
                if ni < 0:
                    raise ValueError("factorial requires non-negative integer")
                if ni > 12:
                    raise ValueError("factorial too large")
                res = 1
                for k in range(2, ni + 1):
                    res *= k
                return res

            def root(a, b):
                if b == 0:
                    raise ZeroDivisionError("0-th root")
                return float(a) ** (1.0 / float(b))

            # Use eval with restricted globals for safety
            allowed_names = {
                "__builtins__": {},
                "abs": abs, "min": min, "max": max,
                "round": round, "int": int, "float": float,
                "fact": fact, "root": root
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
            # Allow factorial option for single digit too
            d = digits[0]
            results = set()
            results.add((str(d), float(d)))
            # try factorial if valid
            try:
                results.add((f"fact({d})", float(eval(str(math.factorial(d))))))
            except Exception:
                pass
            return results
        
        expressions = set()
        
        # Prepare token options per digit to optionally apply factorial
        token_options = [[str(d), f"fact({d})"] for d in digits]

        # Generate all combinations of tokens and operators
        for token_choice in itertools.product(*token_options):
            for operators in itertools.product(self.OPERATORS, repeat=len(digits)-1):
                # Build expression respecting special operators
                expr = str(token_choice[0])
                for i, op in enumerate(operators):
                    next_token = str(token_choice[i + 1])
                    if op == '^':
                        expr += f" ** {next_token}"
                    elif op == 'root':
                        expr = f"root({expr},{next_token})"
                    else:
                        expr += f" {op} {next_token}"

                result = self.safe_eval(expr)
                if result is not None:
                    expressions.add((expr, result))

                # Also try with full parenthesization (left to right)
                if len(digits) > 2:
                    paren_expr = f"({token_choice[0]} {operators[0]} {token_choice[1]})"
                    for i in range(1, len(operators)):
                        if operators[i] == 'root':
                            paren_expr = f"root({paren_expr},{token_choice[i + 1]})"
                        elif operators[i] == '^':
                            paren_expr = f"({paren_expr} ** {token_choice[i + 1]})"
                        else:
                            paren_expr = f"({paren_expr} {operators[i]} {token_choice[i + 1]})"

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

        # Token options to allow factorial
        token_options = [[str(d), f"fact({d})"] for d in digits]

        # Try different token and operator combinations with a few grouping heuristics
        for token_choice in itertools.product(*token_options):
            for operators in itertools.product(self.OPERATORS, repeat=n-1):
                # 1) Base expression (no extra parentheses)
                expr = str(token_choice[0])
                for i, op in enumerate(operators):
                    next_token = str(token_choice[i + 1])
                    if op == '^':
                        expr += f" ** {next_token}"
                    elif op == 'root':
                        expr = f"root({expr},{next_token})"
                    else:
                        expr += f" {op} {next_token}"

                result = self.safe_eval(expr)
                if result is not None:
                    expressions.add((expr, result))

                # 2) Left-associative full parenthesization
                if n > 2:
                    paren_expr = f"({token_choice[0]} {operators[0]} {token_choice[1]})"
                    for i in range(1, len(operators)):
                        if operators[i] == 'root':
                            paren_expr = f"root({paren_expr},{token_choice[i + 1]})"
                        elif operators[i] == '^':
                            paren_expr = f"({paren_expr} ** {token_choice[i + 1]})"
                        else:
                            paren_expr = f"({paren_expr} {operators[i]} {token_choice[i + 1]})"

                    result = self.safe_eval(paren_expr)
                    if result is not None:
                        expressions.add((paren_expr, result))

                # 3) Group first two only
                grouped = f"({token_choice[0]} {operators[0]} {token_choice[1]})"
                for i in range(1, len(operators)):
                    next_token = str(token_choice[i + 1])
                    op = operators[i]
                    if op == '^':
                        grouped = f"{grouped} ** {next_token}"
                    elif op == 'root':
                        grouped = f"root({grouped},{next_token})"
                    else:
                        grouped = f"{grouped} {op} {next_token}"

                result = self.safe_eval(grouped)
                if result is not None:
                    expressions.add((grouped, result))

                # 4) Group last two only
                grouped = str(token_choice[0])
                for i in range(len(operators) - 1):
                    grouped += f" {operators[i]} {token_choice[i + 1]}"
                last_op = operators[-1]
                grouped = f"{grouped} {last_op} ({token_choice[-2]} {last_op} {token_choice[-1]})"
                # Try safe eval
                try:
                    result = self.safe_eval(grouped)
                    if result is not None:
                        expressions.add((grouped, result))
                except Exception:
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