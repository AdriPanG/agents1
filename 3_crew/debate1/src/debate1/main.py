#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from debate1.crew import Debate1
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("GOOGLE_API_KEY"))  # Debe mostrar la clave
print(os.getenv("GEMINI_API_KEY"))  # Si usas este nombre

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'motion': 'There needs to be strict laws to regulate LLMs',
    }
    
    try:
        result = Debate1().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


