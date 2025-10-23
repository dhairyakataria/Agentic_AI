import numexpr as ne
from langchain.tools import tool

@tool
def calculator(expr: str) -> str:
    """Perform mathematical calculations. Input should be a valid mathematical expression."""
    try:
        # numexpr provides safe evaluation (no code execution)
        result = ne.evaluate(expr)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"