#!/usr/bin/env python
import sys
import warnings

from financial_researcher1.crew import FinancialResearcher1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the financial researcher crew.
    """
    inputs = {
        'company': 'Tesla',
    }
    
    result = FinancialResearcher1().crew().kickoff(inputs=inputs)
    print(result.raw)

if __name__ == "__main__":
    run()

