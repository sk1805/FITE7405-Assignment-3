import numpy as np
from scipy.stats import norm

def black_scholes(S, K, r, q, T, sigma, option_type):
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
    option_type : str
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Option price
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
    if sigma <= 0:
        raise ValueError("Volatility sigma must be positive.")
    if option_type.lower() not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'")

    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate discount factors
    disc_S = np.exp(-q * T)
    disc_K = np.exp(-r * T)

    # Calculate option price based on type
    if option_type.lower() == 'call':
        price = S * disc_S * norm.cdf(d1) - K * disc_K * norm.cdf(d2)
    else:  # put option
        price = K * disc_K * norm.cdf(-d2) - S * disc_S * norm.cdf(-d1)

    return round(price, 10)

if __name__ == "__main__":
    try:
        test_cases = [
            # At-the-money options
            (100, 100, 0.05, 0.05, 3, 0.3, "call"),
            (100, 100, 0.05, 0.05, 3, 0.3, "put"),
            # Out-of-the-money options
            (100, 110, 0.05, 0.05, 3, 0.3, "call"),
            (100, 90, 0.05, 0.05, 3, 0.3, "put"),
            # In-the-money options
            (100, 90, 0.05, 0.05, 3, 0.3, "call"),
            (100, 110, 0.05, 0.05, 3, 0.3, "put"),
        ]
        
        print("\nRunning test cases...")
        for S, K, r, q, T, sigma, option_type in test_cases:
            price = black_scholes(S, K, r, q, T, sigma, option_type)
            print(f"\nResults for S: {S}, K: {K}, r: {r}, q: {q}, T: {T}, sigma: {sigma}, option_type: {option_type}")
            print(f"Black-Scholes Option price: {price:.10f}")
            print("--------------------------------", flush=True)

    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 