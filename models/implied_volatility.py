import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from black_scholes import black_scholes

def implied_volatility(S, K, r, q, T, market_price, option_type):
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
    market_price : float
        Option premium
    option_type : str
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Implied volatility
    """
    # Validate input parameters
    if S <= 0:
        raise ValueError("Spot price S must be positive.")
    if K <= 0:
        raise ValueError("Strike price K must be positive.")
    if r < 0 or r > 1:
        raise ValueError("Risk-free rate r must be between 0 and 1.")
    if q < 0:
        raise ValueError("Repo rate q must be non-negative.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if market_price < 0:
        raise ValueError("Market price must be non-negative.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'")

    # Function to calculate the option price using Black-Scholes
    def option_price(sigma):
        return black_scholes(S, K, r, q, T, sigma, option_type)

    # Use Brent's method to find the implied volatility
    try:
        implied_vol = brentq(lambda sigma: option_price(sigma) - market_price, 1e-6, 5)
    except Exception as e:
        raise ValueError(f"Could not calculate implied volatility: {str(e)}")

    return implied_vol

if __name__ == "__main__":
    try:
        test_cases = [
            (100, 100, 0.05, 0.05, 3, 10, "call"),
            (100, 100, 0.05, 0.05, 3, 10, "put"),
        ]
        
        print("\nRunning test cases...")
        for S, K, r, q, T, market_price, option_type in test_cases:
            implied_vol = implied_volatility(S, K, r, q, T, market_price, option_type)
            print(f"\nResults for S: {S}, K: {K}, r: {r}, q: {q}, T: {T}, market_price: {market_price}, option_type: {option_type}")
            print(f"Implied volatility: {implied_vol:.10f}")
            print("--------------------------------")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 