# tools/computation.py

from langchain_experimental.tools import PythonAstTool

def get_computation_tool():
    """
    Initializes and returns the Python Code Execution Tool (Code Interpreter).
    This tool is used for mathematical operations, unit conversions, and numerical logic processing.
    """
    
    # PythonAstTool is the safest tool for executing code in a sandbox environment.
    # The LLM will write Python code, and this tool will execute it.
    return PythonAstTool(
        name="python_calculator",
        description="""
        A powerful Python interpreter. Use this for ANY mathematical calculation, 
        unit conversion, statistical analysis, or complex data manipulation.
        Input should be a single string containing valid Python code (e.g., print(50 * 20)).
        NEVER use external libraries like os, network, or file I/O.
        """
    )