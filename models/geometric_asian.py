import numpy as np
from scipy.stats import norm

def geometric_asian(S0, sigma, r, T, K, n, option_type):
    """
    Calculate the price of a geometric Asian option.
    
    Parameters:
    -----------
    S0 : float
        Spot price of the underlying asset (S(0))
    sigma : float
        Volatility of the underlying asset
    r : float
        Risk-free interest rate
    T : float
        Time to maturity in years
    K : float
        Strike price
    n : int
        Number of observation times for the geometric average
    option_type : str
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Option price
    """
    # Validate input parameters
    if S0 <= 0:
        raise ValueError("Spot price S(0) must be positive.")
    if K <= 0:
        raise ValueError("Strike price K must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility sigma must be positive.")
    if r < 0 or r > 1:
        raise ValueError("Risk-free rate r must be between 0 and 1.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if n <= 0:
        raise ValueError("Number of observation times n must be positive.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'")

    # Calculate adjusted parameters for geometric average
    
    sigma_hat = sigma * np.sqrt((n+1) * (2*n + 1)/(6*n**2))
    mu_hat = (r - 0.5*sigma**2)*(n + 1)/(2*n) + 0.5*sigma_hat**2
    
    # Calculate d1 and d2
    d1 = (np.log(S0/K) + (mu_hat + 0.5*sigma_hat**2)*T) / (sigma_hat*np.sqrt(T))
    d2 = d1 - sigma_hat*np.sqrt(T)
    
    if option_type.lower() == 'call':
        price = np.exp(-r*T) * (S0*np.exp(mu_hat*T)*norm.cdf(d1) - K*norm.cdf(d2))
    elif option_type.lower() == 'put':
        price = np.exp(-r*T) * (K*norm.cdf(-d2) - S0*np.exp(mu_hat*T)*norm.cdf(-d1))
    else:
        raise ValueError("Option type must be either 'call' or 'put'")
    
    return price

if __name__ == "__main__":
    try:
        test_cases = [  
            (100, 0.3, 0.05, 3, 100, 50, "call"),
            (100, 0.3, 0.05, 3, 100, 100, "call"),
            (100, 0.4, 0.05, 3, 100, 50, "call"),
            (100, 0.3, 0.05, 3, 100, 100, "put"),
            (100, 0.4, 0.05, 3, 100, 50, "put"),
            (100, 0.3, 0.05, 3, 100, 50, "put")
        ]
        
        print("\nRunning test cases...")
        for S0, sigma, r, T, K, n, option_type in test_cases:
            price = geometric_asian(S0, sigma, r, T, K, n, option_type)
            print(f"\nResults for S0: {S0}, sigma: {sigma}, r: {r}, T: {T}, K: {K}, n: {n}, option_type: {option_type}")
            print(f"Geometric Asian Option price: {price:.10f}")
            print("--------------------------------")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 