import numpy as np
from scipy.stats import norm

def geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, n, option_type):
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
    n : int
        Number of observation times for the geometric average
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
    if n <= 1:
        raise ValueError("Number of observations n must be greater than 1.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be 'call' or 'put'.")

    # Time step for each observation (equally spaced)
    dt = T / n

    # Simulate paths for both assets and calculate the geometric average
    S1_path = np.zeros(n)
    S2_path = np.zeros(n)
    for i in range(n):
        # Calculate the price at each observation time
        Z1 = np.random.normal(0, 1)
        Z2 = rho * Z1 + np.sqrt(1 - rho**2) * np.random.normal(0, 1)
        S1_path[i] = S1 * np.exp((r - 0.5 * sigma1 ** 2) * (i + 1) * dt + sigma1 * np.sqrt((i + 1) * dt) * Z1)
        S2_path[i] = S2 * np.exp((r - 0.5 * sigma2 ** 2) * (i + 1) * dt + sigma2 * np.sqrt((i + 1) * dt) * Z2)

    # Calculate the geometric average at maturity
    geo_avg = np.exp(np.sum(np.log(S1_path) + np.log(S2_path)) / (2 * n))

    # Calculate option price based on option type
    if option_type == 'call':
        price = np.exp(-r * T) * max(0, geo_avg - K)
    else:  # 'put'
        price = np.exp(-r * T) * max(0, K - geo_avg)

    return price


if __name__ == "__main__":
    try:
       S1 = float(input("Enter spot price of first asset: "))
        S2 = float(input("Enter spot price of second asset: "))
        sigma1 = float(input("Enter volatility of first asset (decimal): "))
        sigma2 = float(input("Enter volatility of second asset (decimal): "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        K = float(input("Enter strike price: "))
        rho = float(input("Enter correlation (decimal): "))
        option_type = input("Enter option type (call/put): ")
            
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