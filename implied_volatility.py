import numpy as np
from scipy.optimize import brentq
from black_scholes import black_scholes

def implied_volatility(S, K, r, q, T, price, option_type='call'):
    """
    Calculate the implied volatility of a European option.
    
    Parameters:
    -----------
    S : float
        Spot price of the underlying asset (S(0))
    K : float
        Strike price
    r : float
        Risk-free interest rate
    q : float
        Repo rate
    T : float
        Time to maturity in years
    price : float
        Option premium
    option_type : str, optional
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Implied volatility
    """
    def f(sigma):
        return black_scholes(S, K, r, q, T, sigma, option_type) - price
    
    try:
        # Use Brent's method to find the root
        iv = brentq(f, 0.0001, 5.0)
        return iv
    except ValueError:
        raise ValueError("No solution exists for the given parameters")

if __name__ == "__main__":
    try:
        S = float(input("Enter spot price: "))
        K = float(input("Enter strike price: "))
        T = float(input("Enter time to maturity (years): "))
        r = float(input("Enter risk-free rate (decimal): "))
        q = float(input("Enter repo rate (decimal): "))
        price = float(input("Enter option premium: "))
        option_type = input("Enter option type (call/put): ").lower()
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        
        iv = implied_volatility(S, K, r, q, T, price, option_type)
        print(f"\nImplied volatility: {iv:.10f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 