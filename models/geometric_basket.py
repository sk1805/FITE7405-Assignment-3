import numpy as np
from scipy.stats import norm

def geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type):
    """
    Calculate the price of a geometric basket option.

    Parameters:
    -----------
    S1 : float
        Spot price of the first asset (S1(0))
    S2 : float
        Spot price of the second asset (S2(0))
    sigma1 : float
        Volatility of the first asset
    sigma2 : float
        Volatility of the second asset
    r : float
        Risk-free interest rate
    T : float
        Time to maturity in years
    K : float
        Strike price
    rho : float
        Correlation between the two assets
    option_type : str
        Type of option ('call' or 'put')
    """
    # Input validation
    if S1 <= 0 or S2 <= 0:
        raise ValueError("Spot prices must be positive.")
    if sigma1 <= 0 or sigma2 <= 0:
        raise ValueError("Volatilities must be positive.")
    if T <= 0:
        raise ValueError("Time to maturity must be positive.")
    if not (-1 <= rho <= 1):
        raise ValueError("Correlation rho must be between -1 and 1.")
    if K <= 0:
        raise ValueError("Strike price must be positive.")
    if r < 0 or r > 1:
        raise ValueError("Risk-free rate r must be between 0 and 1.")
    if rho < -1 or rho > 1:
        raise ValueError("Correlation rho must be between -1 and 1.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be 'call' or 'put'.")

    # Geometric average spot price and effective volatility
    B0 = np.sqrt(S1 * S2)
    sigma_B = np.sqrt((sigma1 ** 2 + sigma2 ** 2 + 2 * rho * sigma1 * sigma2)) / 2

    mu = r - 0.25*(sigma1**2 + sigma2**2) + 0.5*sigma_B**2
    
    # Black-Scholes d1 and d2
    d1 = (np.log(B0 / K) + (mu + 0.5 * sigma_B ** 2) * T) / (sigma_B * np.sqrt(T))
    d2 = d1 - sigma_B * np.sqrt(T)

    # Option price
    if option_type == 'call':
        price = np.exp(-r * T) * (B0 * np.exp(mu * T) * norm.cdf(d1) - K * norm.cdf(d2))
    else:
        price = np.exp(-r * T) * (K * norm.cdf(-d2) - B0 * np.exp(mu * T) * norm.cdf(-d1))

    return price


if __name__ == "__main__":
    try:
        test_cases = [
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, "put"),
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.9, "put"),
            (100, 100, 0.1, 0.3, 0.05, 3, 100, 0.5, "put"),
            (100, 100, 0.3, 0.3, 0.05, 3, 80, 0.5, "put"),
            (100, 100, 0.3, 0.3, 0.05, 3, 120, 0.5, "put"),
            (100, 100, 0.5, 0.5, 0.05, 3, 100, 0.5, "put"),
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, "call"),
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.9, "call"),
            (100, 100, 0.1, 0.3, 0.05, 3, 100, 0.5, "call"),
            (100, 100, 0.3, 0.3, 0.05, 3, 80, 0.5, "call"),
            (100, 100, 0.3, 0.3, 0.05, 3, 120, 0.5, "call"),
            (100, 100, 0.5, 0.5, 0.05, 3, 100, 0.5, "call")
        ]
        
        print("\nRunning test cases...")
        for S1, S2, sigma1, sigma2, r, T, K, rho, option_type in test_cases:
            price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)
            print(f"\nResults for S1: {S1}, S2: {S2}, sigma1: {sigma1}, sigma2: {sigma2}, r: {r}, T: {T}, K: {K}, rho: {rho}, option_type: {option_type}")
            print(f"Geometric Basket Option price: {price:.10f}")
            print("--------------------------------")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 