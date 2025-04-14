#!/usr/bin/env python3
import os
import importlib.util

def run_all_tests():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List of all model files
    model_files = [
        "black_scholes.py",
        "american_binomial.py",
        "arithmetic_asian_mc.py",
        "arithmetic_basket_mc.py",
        "geometric_asian.py",
        "geometric_basket.py",
        "implied_volatility.py",
        "kiko_quasi_mc.py"
    ]
    
    # Save current directory
    original_dir = os.getcwd()
    os.chdir(current_dir)
    
    for model_file in model_files:
        print(f"\n=== Running {model_file.replace('.py', '')} Tests ===")
        try:
            with open(model_file) as f:
                code = compile(f.read(), model_file, 'exec')
                exec(code, {'__name__': '__main__'})
        except Exception as e:
            print(f"Error running {model_file}: {str(e)}")
    
    # Restore original directory
    os.chdir(original_dir)

if __name__ == "__main__":
    print("Starting all model tests...")
    run_all_tests()
    print("\nAll tests completed!") 