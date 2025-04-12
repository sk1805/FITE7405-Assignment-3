import numpy as np
from models.geometric_asian import geometric_asian
from scipy.stats import norm

def arithmetic_asian_mc(S0, sigma, r, T, K, n, option_type, num_simulations, control_variate=None):
    """
    Calculate the price of an arithmetic Asian option using Monte Carlo simulation with control variate.
    
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
        Number of observation times for the arithmetic average
    option_type : str
        Type of option ('call' or 'put')
    num_simulations : int
        Number of simulations for Monte Carlo
    control_variate : str
        Control variate method ('none' or 'geometric')
    
    Returns:
    --------
    tuple
        (Option price, Standard error)
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
    if num_simulations <= 0:
        raise ValueError("Number of simulations must be positive.")
    if control_variate not in ['none', 'geometric']:
        raise ValueError("Control variate method must be either 'none' or 'geometric'.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'.")

    # Set fixed seed for reproducibility
    np.random.seed(42)
    
    dt = T/n
    drift = (r - 0.5*sigma**2)*dt
    vol = sigma*np.sqrt(dt)
    
    # Generate random numbers
    Z = np.random.normal(0, 1, (num_simulations, n))
    
    # Simulate stock paths
    S_paths = np.zeros((num_simulations, n+1))
    S_paths[:, 0] = S0
    
    for i in range(n):
        S_paths[:, i+1] = S_paths[:, i] * np.exp(drift + vol*Z[:, i])
    
    # Calculate arithmetic and geometric averages
    arithmetic_avg = np.mean(S_paths[:, 1:], axis=1)
    geometric_avg = np.exp(np.mean(np.log(S_paths[:, 1:]), axis=1))
    # Calculate payoffs
    if option_type == 'call':
        arithmetic_payoffs = np.maximum(arithmetic_avg - K, 0)
        geometric_payoffs = np.maximum(geometric_avg - K, 0)
    elif option_type == 'put':
        arithmetic_payoffs = np.maximum(K - arithmetic_avg, 0)
        geometric_payoffs = np.maximum(K - geometric_avg, 0)
    else:
        raise ValueError("Invalid option_type. Must be 'call' or 'put'.")

    
    # If control variate is specified, adjust the payoffs
    if control_variate == 'geometric':
        # Calculate the geometric Asian option price
        geometric_price = geometric_asian(S0, sigma, r, T, K, n, option_type)
        
        # Calculate control variate coefficient
        cov = np.cov(arithmetic_payoffs, geometric_payoffs)[0, 1]
        var = np.var(geometric_payoffs)
        beta = cov / var
        
        # Adjust payoffs using control variate
        adjusted_payoffs = arithmetic_payoffs - beta * (geometric_payoffs - geometric_price)
    else:
        adjusted_payoffs = arithmetic_payoffs
    
    # Calculate option price and standard error
    price = np.exp(-r*T) * np.mean(adjusted_payoffs)
    stderr = np.exp(-r*T) * np.std(adjusted_payoffs) / np.sqrt(num_simulations)
    
    return price, stderr

if __name__ == "__main__":
    try:
        S0 = float(input("Enter spot price: "))
        sigma = float(input("Enter volatility (decimal): "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        K = float(input("Enter strike price: "))
        n = int(input("Enter number of observation times: "))
        option_type = input("Enter option type (call/put): ")
        num_simulations = int(input("Enter number of simulations: "))
        control_variate = input("Enter control variate method (none/geometric): ")
        
        price, stderr = arithmetic_asian_mc(S0, sigma, r, T, K, n, option_type, num_simulations, control_variate)
        print(f"\nOption price: {price:.10f}")
        print(f"Standard error: {stderr:.10f}")
        print(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 