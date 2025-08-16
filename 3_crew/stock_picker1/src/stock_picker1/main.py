#!/usr/bin/env python
import sys
import warnings

from stock_picker1.crew import StockPicker1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology',
    }
    
    result = StockPicker1().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()

