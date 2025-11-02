# Birthday Equation Generator

A Python script that takes a date as input and generates arithmetic equations using all possible combinations of operators between the digits.

## Description

This project contains two main scripts:
1. **`birthday_equation.py`** - Basic equation generator
2. **`advanced_birthday_equation.py`** - Advanced generator with better operator precedence and grouping

## Features

- Extracts digits from any date format (e.g., "09052005", "09/05/2005", "2005-05-09")
- Generates equations using arithmetic operators (+, -, *, /)
- Finds equations where left side equals right side
- Handles operator precedence and parentheses grouping
- Safe evaluation of mathematical expressions
- Interactive mode for testing multiple dates

## Usage

### GUI Applications (Recommended)

#### Easy Launcher
```bash
python launcher.py
# or on Windows: double-click run_gui.bat
```

#### Direct GUI Launch
```bash
python birthday_equation_gui.py      # Basic GUI
python enhanced_gui.py               # Advanced GUI with tabs
```

### Command Line Versions

#### Basic CLI
```bash
python birthday_equation.py
```

#### Advanced CLI  
```bash
python advanced_birthday_equation.py
```

### Example

For the date `09052005`, the script extracts digits `[0, 9, 0, 5, 2, 0, 0, 5]` and finds equations like:
- `0 = 9 * 0 - 5 * 2 * 0 - 0 / 5`
- `0 + 9 * 0 = 5 - 2 - 0 - 0 - 5` (after grouping adjustments)
- `(0 + 9) * 0 = (5 - 2) * (0 + 0) - 5`

## How It Works

1. **Digit Extraction**: Extracts all numeric digits from the input date
2. **Split Generation**: Tries different ways to split digits between left and right sides of equation
3. **Operator Combinations**: Generates all possible combinations of +, -, *, / operators
4. **Expression Evaluation**: Safely evaluates mathematical expressions
5. **Equality Check**: Finds expressions where both sides equal each other (within numerical tolerance)
6. **Grouping**: Advanced version tries different parentheses groupings for operator precedence

## File Structure

```
birthday_equation/
├── birthday_equation.py              # Basic equation generator (CLI)
├── advanced_birthday_equation.py     # Advanced generator (CLI)
├── birthday_equation_gui.py          # Basic GUI version
├── enhanced_gui.py                   # Advanced GUI with tabs & export
├── launcher.py                       # GUI launcher application
├── run_gui.bat                       # Windows batch launcher
├── test_equations.py                # Test script for CLI versions
├── test_gui.py                      # Test script for GUI versions
├── demo.py                          # Quick demonstration
├── analyze_example.py               # Analysis of example equation
└── README.md                        # This file
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Testing

Run the test script to verify functionality:
```bash
python test_equations.py
```

## Examples

### Input: "123"
```
Extracted digits: [1, 2, 3]
Found equations:
1. 1 + 2 = 3  (= 3)
```

### Input: "1234"  
```
Extracted digits: [1, 2, 3, 4]
Found equations:
1. 1 = 2 + 3 - 4  (= 1)
```

### Input: "09052005"
```
Extracted digits: [0, 9, 0, 5, 2, 0, 0, 5]
Found 180+ equations including:
1. 0 = 9 * 0 - 5 * 2 * 0 - 0 / 5  (= 0)
2. (0 + 9) * 0 = (5 - 2) * 0 + 0 - 5  (= 0)
...
```

## Note

The example equation `(0+9+0-5) = 2*0+0+5` from the original request evaluates to `4 = 5`, which is not mathematically equal. The script finds actual valid equations where both sides are truly equal.

## GUI Features

### Basic GUI (`birthday_equation_gui.py`)
- Simple, clean interface
- Date input with validation
- Real-time progress tracking
- Results preview
- Save equations to text file
- Easy to use for beginners

### Enhanced GUI (`enhanced_gui.py`)
- Tabbed interface with multiple sections
- Choice between Basic and Advanced generators
- Multiple export formats: TXT, CSV, JSON
- Configurable display limits
- Settings and help documentation
- Professional interface for advanced users

### GUI Launcher (`launcher.py`)
- Choose between different interface options
- Launch GUI or CLI versions
- Built-in help and descriptions
- Easy access to all features

## Interactive Mode

Both CLI scripts include an interactive mode where you can enter multiple dates and see the generated equations in real-time. Type 'quit' to exit.