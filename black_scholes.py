import numpy as np
from scipy.stats import norm

def black_scholes(S, K, r, q, T, sigma, option_type='call'):
    """
    Calculate the price of a European option using the Black-Scholes model.
    
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
    sigma : float
        Volatility of the underlying asset
    option_type : str, optional
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Option price
    """
    d1 = (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type.lower() == 'call':
        price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("Option type must be either 'call' or 'put'")
    
    return price

def run():
    print("\nBlack-Scholes European Option Pricing")
    print("=====================================")
    
    try:
        S = float(input("Enter current stock price: "))
        K = float(input("Enter strike price: "))
        T = float(input("Enter time to maturity (years): "))
        r = float(input("Enter risk-free rate (decimal): "))
        q = float(input("Enter repo rate (decimal): "))
        sigma = float(input("Enter volatility (decimal): "))
        option_type = input("Enter option type (call/put): ").lower()
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        
        price = black_scholes(S, K, r, q, T, sigma, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 