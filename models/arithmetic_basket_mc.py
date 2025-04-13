import numpy as np
from geometric_basket import geometric_basket
from typing import Tuple, List

def arithmetic_basket_mc(S1: float, S2: float, sigma1: float, sigma2: float, r: float, T: float, K: float, rho: float, 
                        option_type: str, num_simulations: int, control_variate: str) -> Tuple[float, float, List[float]]:
    """
    Calculate the price of an arithmetic basket option using Monte Carlo simulation.

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
        Option type ('call' or 'put')
    num_simulations : int
        Number of simulations for Monte Carlo
    control_variate : str
        Control variate method ('none' or 'geometric')

    Returns:
    --------
    Tuple[float, float, List[float]]
        (Option price, Standard error, 95% Confidence interval [lower, upper])
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
    if r < 0 or r > 1:
        raise ValueError("Risk-free rate r must be between 0 and 1.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if K <= 0:
        raise ValueError("Strike price K must be positive.")
    if not (-1 <= rho <= 1):
        raise ValueError("Correlation rho must be between -1 and 1.")
    if num_simulations <= 0:
        raise ValueError("Number of simulations must be positive.")
    if control_variate not in ['none', 'geometric']:
        raise ValueError("Control variate method must be either 'none' or 'geometric'.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'.")

    # Set seed for reproducibility
    np.random.seed(5)

    # Simulate correlated standard normals
    Z1 = np.random.normal(0, 1, num_simulations)
    Z2 = rho * Z1 + np.sqrt(1 - rho**2) * np.random.normal(0, 1, num_simulations)

    # Simulate asset prices at maturity
    S1_T = S1 * np.exp((r - 0.5 * sigma1**2) * T + sigma1 * np.sqrt(T) * Z1)
    S2_T = S2 * np.exp((r - 0.5 * sigma2**2) * T + sigma2 * np.sqrt(T) * Z2)

    # Arithmetic average basket
    arithmetic_avg = 0.5 * (S1_T + S2_T)

    # Payoffs
    if option_type == 'call':
        payoffs = np.maximum(arithmetic_avg - K, 0)
    else:
        payoffs = np.maximum(K - arithmetic_avg, 0)

    # Control variate method using geometric basket
    if control_variate == 'geometric':
        # Geometric average
        geo_avg = np.sqrt(S1_T * S2_T)
        if option_type == 'call':
            geo_payoffs = np.maximum(geo_avg - K, 0)
        else:
            geo_payoffs = np.maximum(K - geo_avg, 0)

        # Get discounted payoffs first
        discounted_payoffs = np.exp(-r * T) * payoffs
        discounted_geo_payoffs = np.exp(-r * T) * geo_payoffs

        # Analytical price of geometric basket option
        geo_price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)

        # Control variate adjustment (using discounted payoffs)
        cov = np.cov(discounted_payoffs, discounted_geo_payoffs)[0, 1]
        var_geo = np.var(discounted_geo_payoffs)
        beta = cov / var_geo

        # Apply control variate adjustment to discounted payoffs
        price = np.mean(discounted_payoffs - beta * (discounted_geo_payoffs - geo_price))
        stderr = np.std(discounted_payoffs - beta * (discounted_geo_payoffs - geo_price)) / np.sqrt(num_simulations)
    else:
        # Standard Monte Carlo
        price = np.exp(-r * T) * np.mean(payoffs)
        stderr = np.exp(-r * T) * np.std(payoffs) / np.sqrt(num_simulations)

    # Calculate 95% confidence interval
    conf_interval = [price - 1.96 * stderr, price + 1.96 * stderr]

    return price, stderr, conf_interval

if __name__ == "__main__":
    try:
        test_cases = [
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, "put", 100000, "geometric"),
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.9, "put", 100000, "geometric"),
            (100, 100, 0.1, 0.3, 0.05, 3, 100, 0.5, "put", 100000, "geometric"),
            (100, 100, 0.3, 0.3, 0.05, 3, 80, 0.5, "put", 100000, "geometric"),
            (100, 100, 0.3, 0.3, 0.05, 3, 120, 0.5, "put", 100000, "geometric"),
            (100, 100, 0.5, 0.5, 0.05, 3, 100, 0.5, "put", 100000, "geometric"),
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, "call", 100000, "geometric"),
            (100, 100, 0.3, 0.3, 0.05, 3, 100, 0.9, "call", 100000, "geometric"),
            (100, 100, 0.1, 0.3, 0.05, 3, 100, 0.5, "call", 100000, "geometric"),
            (100, 100, 0.3, 0.3, 0.05, 3, 80, 0.5, "call", 100000, "geometric"),
            (100, 100, 0.3, 0.3, 0.05, 3, 120, 0.5, "call", 100000, "geometric"),
            (100, 100, 0.5, 0.5, 0.05, 3, 100, 0.5, "call", 100000, "geometric")

        ]

        print("\nRunning test cases...")
        for S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate in test_cases:
            price, stderr, conf_interval = arithmetic_basket_mc(S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate)
            geo_price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)
            print(f"\nResults for S1: {S1}, S2: {S2}, sigma1: {sigma1}, sigma2: {sigma2}, r: {r}, T: {T}, K: {K}, rho: {rho}, option_type: {option_type}, num_simulations: {num_simulations}, control_variate: {control_variate}")
            print(f"Arithmetic Basket Option price: {price:.10f}")
            print(f"Standard error: {stderr:.10f}")
            print(f"95% Confidence Interval: [{conf_interval[0]:.10f}, {conf_interval[1]:.10f}]")
            print(f"Geometric Basket Option price: {geo_price:.10f}")
            print("--------------------------------")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 