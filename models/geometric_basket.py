import numpy as np
from scipy.stats import norm

def geometric_basket(S1, S2, K, r, T, sigma1, sigma2, rho, option_type='call'):
    """
    Calculate the price of a geometric basket option.
    
    Parameters:
    -----------
    S1 : float
        Spot price of the first underlying asset (S1(0))
    S2 : float
        Spot price of the second underlying asset (S2(0))
    K : float
        Strike price
    r : float
        Risk-free interest rate
    T : float
        Time to maturity in years
    sigma1 : float
        Volatility of the first underlying asset
    sigma2 : float
        Volatility of the second underlying asset
    rho : float
        Correlation between the two underlying assets
    option_type : str, optional
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Option price
    """
    # Calculate geometric average of initial prices
    S0 = np.sqrt(S1 * S2)
    
    # Calculate adjusted parameters for geometric basket
    sigma = np.sqrt(0.5 * (sigma1**2 + sigma2**2 + 2*rho*sigma1*sigma2))
    mu = r - 0.5 * (sigma1**2 + sigma2**2)/2 + 0.5 * sigma**2
    
    # Calculate d1 and d2
    d1 = (np.log(S0/K) + (mu + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type.lower() == 'call':
        price = np.exp(-r*T) * (S0*np.exp(mu*T)*norm.cdf(d1) - K*norm.cdf(d2))
    elif option_type.lower() == 'put':
        price = np.exp(-r*T) * (K*norm.cdf(-d2) - S0*np.exp(mu*T)*norm.cdf(-d1))
    else:
        raise ValueError("Option type must be either 'call' or 'put'")
    
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
        
        price = geometric_basket(S1, S2, K, r, T, sigma1, sigma2, rho, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 