import numpy as np
from scipy.stats import norm

def geometric_asian(S, K, r, T, sigma, n, option_type='call'):
    """
    Calculate the price of a geometric Asian option.
    
    Parameters:
    -----------
    S : float
        Spot price of the underlying asset (S(0))
    K : float
        Strike price
    r : float
        Risk-free interest rate
    T : float
        Time to maturity in years
    sigma : float
        Volatility of the underlying asset
    n : int
        Number of observation times
    option_type : str, optional
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Option price
    """
    # Calculate adjusted parameters for geometric average
    sigma_hat = sigma * np.sqrt((2*n + 1)/(6*(n + 1)))
    mu_hat = (r - 0.5*sigma**2)*(n + 1)/(2*n) + 0.5*sigma_hat**2
    
    # Calculate d1 and d2
    d1 = (np.log(S/K) + (mu_hat + 0.5*sigma_hat**2)*T) / (sigma_hat*np.sqrt(T))
    d2 = d1 - sigma_hat*np.sqrt(T)
    
    if option_type.lower() == 'call':
        price = np.exp(-r*T) * (S*np.exp(mu_hat*T)*norm.cdf(d1) - K*norm.cdf(d2))
    elif option_type.lower() == 'put':
        price = np.exp(-r*T) * (K*norm.cdf(-d2) - S*np.exp(mu_hat*T)*norm.cdf(-d1))
    else:
        raise ValueError("Option type must be either 'call' or 'put'")
    
    return price

if __name__ == "__main__":
    try:
        S = float(input("Enter spot price: "))
        K = float(input("Enter strike price: "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        sigma = float(input("Enter volatility (decimal): "))
        n = int(input("Enter number of observation times: "))
        option_type = input("Enter option type (call/put): ").lower()
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        
        price = geometric_asian(S, K, r, T, sigma, n, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 