import numpy as np
from scipy.stats import norm
from scipy.stats import qmc

def kiko_quasi_mc(S, K, r, T, sigma, L, U, R, n, calculate_delta=False):
    """
    Calculate the price of a KIKO (Knock-In Knock-Out) put option using quasi-Monte Carlo simulation.
    
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
    L : float
        Lower barrier
    U : float
        Upper barrier
    R : float
        Cash rebate
    n : int
        Number of observation times
    calculate_delta : bool, optional
        Whether to calculate Delta (default: False)
    
    Returns:
    --------
    tuple
        (Option price, Standard error, Delta) if calculate_delta is True
        (Option price, Standard error) otherwise
    """
    # Set fixed seed for reproducibility
    np.random.seed(42)
    
    # Validate input parameters
    if S <= 0:
        raise ValueError("Spot price S must be positive.")
    if K <= 0:
        raise ValueError("Strike price K must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility sigma must be positive.")
    if r < 0:
        raise ValueError("Risk-free rate r must be non-negative.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if L >= U:
        raise ValueError("Lower barrier L must be less than upper barrier U.")
    if R < 0:
        raise ValueError("Cash rebate R must be non-negative.")
    if n <= 0:
        raise ValueError("Number of observation times n must be positive.")
    
    dt = T/n
    drift = (r - 0.5*sigma**2)*dt
    vol = sigma*np.sqrt(dt)
    
    # Generate quasi-random numbers using Sobol sequence
    sobol = qmc.Sobol(n, scramble=True)
    Z = norm.ppf(sobol.random(10000))  # Using 10,000 paths
    
    # Simulate stock paths
    S_paths = np.zeros((10000, n+1))
    S_paths[:, 0] = S
    
    for i in range(n):
        S_paths[:, i+1] = S_paths[:, i] * np.exp(drift + vol*Z[:, i])
    
    # Check for knock-in and knock-out conditions
    knock_in = np.any(S_paths <= L, axis=1)
    knock_out = np.any(S_paths >= U, axis=1)
    
    # Calculate payoffs
    payoffs = np.zeros(10000)
    
    # Payoff for paths that knock out
    payoffs[knock_out] = R
    
    # Payoff for paths that knock in but don't knock out
    active_paths = ~knock_out & knock_in
    payoffs[active_paths] = np.maximum(K - S_paths[active_paths, -1], 0)
    
    # Calculate option price and standard error
    price = np.exp(-r*T) * np.mean(payoffs)
    stderr = np.exp(-r*T) * np.std(payoffs) / np.sqrt(10000)
    
    if not calculate_delta:
        return price, stderr
    
    # Calculate Delta using finite difference method
    h = S * 0.01  # 1% of spot price
    price_up, _ = kiko_quasi_mc(S + h, K, r, T, sigma, L, U, R, n)
    price_down, _ = kiko_quasi_mc(S - h, K, r, T, sigma, L, U, R, n)
    delta = (price_up - price_down) / (2 * h)
    
    return price, stderr, delta

if __name__ == "__main__":
    try:
        S = float(input("Enter spot price: "))
        K = float(input("Enter strike price: "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        sigma = float(input("Enter volatility (decimal): "))
        L = float(input("Enter lower barrier: "))
        U = float(input("Enter upper barrier: "))
        R = float(input("Enter cash rebate: "))
        n = int(input("Enter number of observation times: "))
        
        if L >= U:
            raise ValueError("Lower barrier must be less than upper barrier")
        if R < 0:
            raise ValueError("Cash rebate must be non-negative")
        
        price, stderr, delta = kiko_quasi_mc(S, K, r, T, sigma, L, U, R, n, calculate_delta=True)
        print(f"\nOption price: {price:.10f}")
        print(f"Standard error: {stderr:.10f}")
        print(f"Delta: {delta:.10f}")
        print(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 