import numpy as np
from scipy.stats import norm
from scipy.stats import qmc
from typing import Dict, Tuple, Union

# Set fixed seed for reproducibility at module level
np.random.seed(5)

def simulate_paths(S: float, r: float, sigma: float, T: float, n: int, M: int, Z: np.ndarray) -> np.ndarray:
    """Simulate stock price paths using quasi-Monte Carlo."""
    dt = T/n
    drift = (r - 0.5*sigma**2)*dt
    vol = sigma*np.sqrt(dt)
    
    paths = np.zeros((M, n+1))
    paths[:, 0] = S
    
    for i in range(n):
        paths[:, i+1] = paths[:, i] * np.exp(drift + vol*Z[:, i])
    
    return paths

def calculate_payoffs(paths: np.ndarray, K: float, L: float, U: float, R: float, r: float, T: float, n: int) -> np.ndarray:
    """Calculate payoffs for KIKO put option."""
    dt = T/n
    M = paths.shape[0]
    payoffs = np.zeros(M)
    
    # Check for knock-in and knock-out conditions with small epsilon for numerical stability
    eps = 1e-8
    knock_in = np.any(paths <= L + eps, axis=1)
    knock_out = np.any(paths >= U - eps, axis=1)
    
    # Payoff for paths that knock out
    payoffs[knock_out] = R
    
    # Payoff for paths that knock in but don't knock out
    active_paths = ~knock_out & knock_in
    payoffs[active_paths] = np.maximum(K - paths[active_paths, -1], 0)
    
    return payoffs

def kiko_quasi_mc(S: float, K: float, r: float, T: float, sigma: float, L: float, U: float, R: float, n: int, calculate_delta: bool = False) -> Union[Tuple[float, float, Tuple[float, float]], Tuple[float, float, Tuple[float, float], float]]:
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
        (Option price, Standard error, Confidence interval, Delta) if calculate_delta is True
        (Option price, Standard error, Confidence interval) otherwise
    """
    # Validate input parameters
    if S <= 0:
        raise ValueError("Spot price S must be positive.")
    if K <= 0:
        raise ValueError("Strike price K must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility sigma must be positive.")
    if r < 0 or r > 1:
        raise ValueError("Risk-free rate r must be between 0 and 1.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if L >= U:
        raise ValueError("Lower barrier L must be less than upper barrier U.")
    if R < 0:
        raise ValueError("Cash rebate R must be non-negative.")
    if n <= 0:
        raise ValueError("Number of observation times n must be positive.")

    M = 100000  # Number of simulation paths
    
    # Generate quasi-random numbers using Sobol sequence with scrambling
    sobol = qmc.Sobol(n, scramble=True, seed=5)
    Z = norm.ppf(sobol.random(M))
    
    # Simulate stock paths
    paths = simulate_paths(S, r, sigma, T, n, M, Z)
    
    # Calculate payoffs
    payoffs = calculate_payoffs(paths, K, L, U, R, r, T, n)
    
    # Calculate option price and standard error
    price = np.exp(-r*T) * np.mean(payoffs)
    stderr = np.exp(-r*T) * np.std(payoffs) / np.sqrt(M)
    
    # Calculate 95% confidence interval
    conf_interval = (price - 1.96 * stderr, price + 1.96 * stderr)
    
    if not calculate_delta:
        return price, stderr, conf_interval
    
    # Calculate Delta using finite difference method
    h = S * 0.01  # 1% of spot price
    
    # Use new Sobol sequences for up and down prices with different seeds
    sobol_up = qmc.Sobol(n, scramble=True, seed=6)
    Z_up = norm.ppf(sobol_up.random(M))
    paths_up = simulate_paths(S + h, r, sigma, T, n, M, Z_up)
    payoffs_up = calculate_payoffs(paths_up, K, L, U, R, r, T, n)
    price_up = np.exp(-r*T) * np.mean(payoffs_up)
    
    sobol_down = qmc.Sobol(n, scramble=True, seed=7)
    Z_down = norm.ppf(sobol_down.random(M))
    paths_down = simulate_paths(S - h, r, sigma, T, n, M, Z_down)
    payoffs_down = calculate_payoffs(paths_down, K, L, U, R, r, T, n)
    price_down = np.exp(-r*T) * np.mean(payoffs_down)
    
    delta = (price_up - price_down) / (2 * h)
    
    return price, stderr, conf_interval, delta

if __name__ == "__main__":
    try:
        test_cases = [
            (100, 100, 0.05, 2, 0.2, 80, 125, 1.5, 24, True),
            (100, 100, 0.03, 2, 0.2, 75, 105, 5, 24, True),
        ]
        
        for S, K, r, T, sigma, L, U, R, n, calculate_delta in test_cases:
            price, stderr, conf_interval, delta = kiko_quasi_mc(S, K, r, T, sigma, L, U, R, n, calculate_delta)
            print(f"\nResults for S: {S}, K: {K}, r: {r}, T: {T}, sigma: {sigma}, L: {L}, U: {U}, R: {R}, n: {n}, calculate_delta: {calculate_delta}")
            print(f"KIKO Option price: {price:.10f}")
            print(f"Standard error: {stderr:.10f}")
            print(f"95% Confidence Interval: [{conf_interval[0]:.10f}, {conf_interval[1]:.10f}]")
            print(f"Delta: {delta:.10f}")
            print("--------------------------------")

        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 