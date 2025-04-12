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
    # Validate input parameters
    if S1 <= 0:
        raise ValueError("Spot price S1(0) must be positive.")
    if S2 <= 0:
        raise ValueError("Spot price S2(0) must be positive.")
    if sigma1 <= 0:
        raise ValueError("Volatility sigma1 must be positive.")
    if sigma2 <= 0:
        raise ValueError("Volatility sigma2 must be positive.")
    if r < 0:
        raise ValueError("Risk-free rate r must be non-negative.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if K <= 0:
        raise ValueError("Strike price K must be positive.")
    if not (-1 <= rho <= 1):
        raise ValueError("Correlation rho must be between -1 and 1.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'.")

    # Calculate d1 and d2 for the geometric basket option
    sigma_g = np.sqrt((sigma1 ** 2 + sigma2 ** 2 + 2 * rho * sigma1 * sigma2))
    d1 = (np.log(S1 / S2) + (r + 0.5 * sigma_g ** 2) * T) / (sigma_g * np.sqrt(T))
    d2 = d1 - sigma_g * np.sqrt(T)

    # Calculate option price based on type
    if option_type == 'call':
        price = np.exp(-r * T) * (S1 * norm.cdf(d1) - K * norm.cdf(d2))
    else:
        price = np.exp(-r * T) * (K * norm.cdf(-d2) - S1 * norm.cdf(-d1))

    return price

if __name__ == "__main__":
    try:
        S1 = float(input("Enter spot price of first asset: "))
        S2 = float(input("Enter spot price of second asset: "))
        K = float(input("Enter strike price: "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        sigma1 = float(input("Enter volatility of first asset (decimal): "))
        sigma2 = float(input("Enter volatility of second asset (decimal): "))
        rho = float(input("Enter correlation between assets (decimal): "))
        option_type = input("Enter option type (call/put): ").lower()
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        if rho < -1 or rho > 1:
            raise ValueError("Correlation must be between -1 and 1")
        
        price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 