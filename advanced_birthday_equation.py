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
    
    def generate_digit_partitions(self, max_groups: int = 5) -> List[List[int]]:
        """
        Generate different ways to partition digits into multi-digit numbers.
        Advanced version with more sophisticated partitioning.
        
        Args:
            max_groups: Maximum number of groups to create
            
        Returns:
            List of partitions, where each partition is a list of multi-digit numbers
        """
        if len(self.digits) <= 1:
            return [[self.digits[0]] if self.digits else []]
        
        partitions = []
        digit_string = ''.join(map(str, self.digits))
        
        def generate_splits(s: str, current_partition: List[int], start_pos: int):
            if start_pos == len(s):
                if len(current_partition) >= 2 and len(current_partition) <= max_groups:
                    partitions.append(current_partition[:])
                return
            
            # Try different lengths for the next number
            max_length = min(4, len(s) - start_pos)  # Cap at 4 digits per number
            
            for length in range(1, max_length + 1):
                # Skip if this would leave insufficient digits for remaining groups
                remaining_digits = len(s) - start_pos - length
                current_groups = len(current_partition) + 1
                
                if remaining_digits > 0 and (max_groups - current_groups) < 1:
                    continue
                if remaining_digits > (max_groups - current_groups) * 4:
                    continue
                
                next_num_str = s[start_pos:start_pos + length]
                next_num = int(next_num_str)
                
                # Avoid numbers that are too large
                if next_num > 9999:
                    continue
                
                current_partition.append(next_num)
                generate_splits(s, current_partition, start_pos + length)
                current_partition.pop()
        
        generate_splits(digit_string, [], 0)
        
        # Always include the original single-digit partition
        partitions.append(self.digits[:])
        
        # Add some common patterns for dates
        if len(self.digits) == 8:  # Date format like 09052005
            # Try DD MM YYYY patterns
            d_str = digit_string
            partitions.append([int(d_str[:2]), int(d_str[2:4]), int(d_str[4:])])  # 09, 05, 2005
            partitions.append([int(d_str[0]), int(d_str[1:3]), int(d_str[3:5]), int(d_str[5:])])  # 0, 90, 52, 005
            partitions.append([int(d_str[:1]), int(d_str[1:4]), int(d_str[4:])])  # 0, 905, 2005
        
        # Remove duplicates
        unique_partitions = []
        seen = set()
        
        for partition in partitions:
            partition_tuple = tuple(partition)
            if partition_tuple not in seen:
                seen.add(partition_tuple)
                unique_partitions.append(partition)
        
        # Sort by partition diversity (prefer mixed digit counts)
        unique_partitions.sort(key=lambda p: (len(p), -sum(1 for x in p if x > 9)))
        
        return unique_partitions
    
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
    
    def generate_all_expressions(self, numbers: List[int]) -> Set[Tuple[str, float]]:
        """Generate all possible expressions from numbers with different operator combinations."""
        if len(numbers) == 1:
            # Allow factorial option for single digit only
            num = numbers[0]
            results = set()
            results.add((str(num), float(num)))
            
            # Only try factorial for single digits (0-9)
            if 0 <= num <= 9:
                try:
                    factorial_val = math.factorial(num)
                    if factorial_val <= 1000000:  # Reasonable limit
                        results.add((f"fact({num})", float(factorial_val)))
                except Exception:
                    pass
            return results
        
        expressions = set()
        
        # Prepare token options per number to optionally apply factorial (only for single digits)
        token_options = []
        for num in numbers:
            if 0 <= num <= 9:
                token_options.append([str(num), f"fact({num})"])
            else:
                token_options.append([str(num)])

        # Generate all combinations of tokens and operators
        for token_choice in itertools.product(*token_options):
            for operators in itertools.product(self.OPERATORS, repeat=len(numbers)-1):
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
                if len(numbers) > 2:
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
    
    def generate_with_custom_grouping(self, numbers: List[int]) -> Set[Tuple[str, float]]:
        """Generate expressions with various custom groupings."""
        if len(numbers) <= 2:
            return self.generate_all_expressions(numbers)

        expressions = set()
        n = len(numbers)

        # Token options to allow factorial (only for single digits)
        token_options = []
        for num in numbers:
            if 0 <= num <= 9:
                token_options.append([str(num), f"fact({num})"])
            else:
                token_options.append([str(num)])

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
        """Find equations where left side equals right side using advanced partitioning."""
        equations = []
        
        # Generate different digit partitions (including advanced splitting)
        partitions = self.generate_digit_partitions()
        
        for partition in partitions:
            # Try different split points within this partition
            for split in range(1, len(partition)):
                left_numbers = partition[:split]
                right_numbers = partition[split:]
                
                # Generate all possible expressions for both sides
                left_expressions = self.generate_all_expressions(left_numbers)
                right_expressions = self.generate_all_expressions(right_numbers)
                
                # Find matching values
                for left_expr, left_val in left_expressions:
                    for right_expr, right_val in right_expressions:
                        if abs(left_val - right_val) <= tolerance:
                            equations.append((left_expr, right_expr, left_val))
        
        return equations
    
    def find_creative_equations(self, tolerance: float = 1e-10) -> List[Tuple[str, str, float]]:
        """Find more creative equations with different digit arrangements and partitions."""
        equations = []
        
        # Generate different digit partitions for creative equations
        partitions = self.generate_digit_partitions(max_groups=6)  # Allow more groups for creativity
        
        for partition in partitions:
            # Multiple split attempts within each partition
            for split in range(1, len(partition)):
                left_numbers = partition[:split]
                right_numbers = partition[split:]
                
                # Use custom grouping
                left_expressions = self.generate_with_custom_grouping(left_numbers)
                right_expressions = self.generate_with_custom_grouping(right_numbers)
                
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
        
        # Show different digit partitions
        partitions = generator.generate_digit_partitions()
        print(f"Generated {len(partitions)} different digit partitions:")
        for i, partition in enumerate(partitions[:10]):  # Show first 10
            print(f"  {i+1}. {partition}")
        if len(partitions) > 10:
            print(f"  ... and {len(partitions) - 10} more partitions")
        print()
        
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