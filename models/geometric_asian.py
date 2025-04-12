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
    if r < 0:
        raise ValueError("Risk-free rate r must be non-negative.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if n <= 0:
        raise ValueError("Number of observation times n must be positive.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'")

    # Calculate adjusted parameters for geometric average
    sigma_hat = sigma * np.sqrt((2*n + 1)/(6*(n + 1)))
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
        S0 = float(input("Enter spot price: "))
        sigma = float(input("Enter volatility (decimal): "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        K = float(input("Enter strike price: "))
        n = int(input("Enter number of observation times: "))
        option_type = input("Enter option type (call/put): ")
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        
        price = geometric_asian(S0, sigma, r, T, K, n, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 