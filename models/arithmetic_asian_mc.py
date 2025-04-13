import numpy as np
from models.geometric_asian import geometric_asian
from scipy.stats import norm
from typing import Tuple, Dict

def simulate_paths(S0: float, sigma: float, r: float, T: float, n: int, num_simulations: int) -> np.ndarray:
    """
    Simulate stock price paths using Monte Carlo simulation.
    
    Parameters:
    -----------
    S0 : float
        Initial stock price
    sigma : float
        Volatility of the underlying asset
    r : float
        Risk-free interest rate
    T : float
        Time to maturity in years
    n : int
        Number of time steps
    num_simulations : int
        Number of Monte Carlo simulations
    
    Returns:
    --------
    np.ndarray
        Array of simulated stock price paths
    """
    np.random.seed(5)  # Set seed for reproducibility
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
    
    return S_paths[:, 1:]  # Exclude the initial price

def compute_payoffs(paths: np.ndarray, K: float, T: float, r: float, option_type: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute arithmetic and geometric payoffs for the paths.
    
    Parameters:
    -----------
    paths : np.ndarray
        Array of simulated stock price paths
    K : float
        Strike price
    T : float
        Time to maturity in years
    r : float
        Risk-free interest rate
    option_type : str
        Type of option ('call' or 'put')
    
    Returns:
    --------
    Tuple[np.ndarray, np.ndarray]
        Arrays of arithmetic and geometric payoffs
    """
    arithmetic_avg = np.mean(paths, axis=1)
    geometric_avg = np.exp(np.mean(np.log(paths), axis=1))
    
    discount = np.exp(-r*T)
    if option_type == 'call':
        arithmetic_payoffs = discount * np.maximum(arithmetic_avg - K, 0)
        geometric_payoffs = discount * np.maximum(geometric_avg - K, 0)
    else:  # put
        arithmetic_payoffs = discount * np.maximum(K - arithmetic_avg, 0)
        geometric_payoffs = discount * np.maximum(K - geometric_avg, 0)
    
    return arithmetic_payoffs, geometric_payoffs

def arithmetic_asian_mc(S0: float, sigma: float, r: float, T: float, K: float, n: int, 
                       option_type: str, num_simulations: int, control_variate: str = None) -> Tuple[float, float]:
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
    Tuple[float, float]
        (Option price, Standard error)
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
    if num_simulations <= 0:
        raise ValueError("Number of simulations must be positive.")
    if control_variate not in ['none', 'geometric']:
        raise ValueError("Control variate method must be either 'none' or 'geometric'.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'.")

    # Simulate stock price paths
    paths = simulate_paths(S0, sigma, r, T, n, num_simulations)
    
    # Calculate arithmetic and geometric payoffs
    arithmetic_payoffs, geometric_payoffs = compute_payoffs(paths, K, T, r, option_type)
    
    # If control variate is specified, adjust the payoffs
    if control_variate == 'geometric':
        # Calculate the geometric Asian option price
        geometric_price = geometric_asian_exact(S0, sigma, r, T, K, n, option_type)
        
        # Calculate control variate coefficient (theta)
        covXY = np.cov(arithmetic_payoffs, geometric_payoffs)[0, 1]
        theta = covXY / np.var(geometric_payoffs)
        
        # Adjust payoffs using control variate
        adjusted_payoffs = arithmetic_payoffs + theta * (geometric_price - geometric_payoffs)
    else:
        adjusted_payoffs = arithmetic_payoffs
    
    # Calculate option price and standard error
    price = np.mean(adjusted_payoffs)
    stderr = np.std(adjusted_payoffs) / np.sqrt(num_simulations)
    
    return price, stderr

def geometric_asian_exact(S0: float, sigma: float, r: float, T: float, K: float, n: int, option_type: str) -> float:
    """
    Calculate the exact price of a geometric Asian option.
    
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
        Exact price of the geometric Asian option
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
        raise ValueError("Option type must be either 'call' or 'put'.")
    
    # Calculate parameters for the geometric Asian option
    sigsqT = sigma**2 * T * (n + 1) * (2 * n + 1) / (6 * n**2)
    muT = 0.5 * sigsqT + (r - 0.5 * sigma**2) * T * (n + 1) / (2 * n)
    
    # Calculate d1 and d2
    d1 = (np.log(S0 / K) + (muT + 0.5 * sigsqT)) / np.sqrt(sigsqT)
    d2 = d1 - np.sqrt(sigsqT)
    
    # Calculate option price
    if option_type == 'call':
        N1 = norm.cdf(d1)
        N2 = norm.cdf(d2)
        price = np.exp(-r * T) * (S0 * np.exp(muT) * N1 - K * N2)
    else:  # put
        N1 = norm.cdf(-d1)
        N2 = norm.cdf(-d2)
        price = np.exp(-r * T) * (K * N2 - S0 * np.exp(muT) * N1)
    
    return price

if __name__ == "__main__":
    try:
        # Test cases
        test_cases = [
            (100, 0.3, 0.05, 3, 100, 50, "call"),
            (100, 0.3, 0.05, 3, 100, 100, "call"),
            (100, 0.4, 0.05, 3, 100, 50, "call"),
            (100, 0.3, 0.05, 3, 100, 100, "put"),
            (100, 0.4, 0.05, 3, 100, 50, "put"),
            (100, 0.3, 0.05, 3, 100, 50, "put")
        ]
        
        num_simulations = 100000
        
        print("\nRunning test cases...")
        for S0, sigma, r, T, K, n, option_type in test_cases:
            # Calculate arithmetic Asian option price with control variate
            price, stderr = arithmetic_asian_mc(S0, sigma, r, T, K, n, option_type, num_simulations, "geometric")
            
            # Calculate geometric Asian option price (exact)
            geo_price = geometric_asian_exact(S0, sigma, r, T, K, n, option_type)
            
            print(f"\nResults for S={S0}, sigma={sigma}, K={K}, n={n}, option_type={option_type}:")
            print(f"Arithmetic Asian Option Price: {price:.6f}")
            print(f"Standard Error: {stderr:.6f}")
            print(f"95% Confidence Interval: [{price-1.96*stderr:.6f}, {price+1.96*stderr:.6f}]")
            print(f"Geometric Asian Option Price (Exact): {geo_price:.6f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 