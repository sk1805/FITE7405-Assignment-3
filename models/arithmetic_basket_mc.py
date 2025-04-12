import numpy as np
from models.geometric_basket import geometric_basket

def arithmetic_basket_mc(S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate):
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
    if num_simulations <= 0:
        raise ValueError("Number of simulations must be positive.")
    if control_variate not in ['none', 'geometric']:
        raise ValueError("Control variate method must be either 'none' or 'geometric'.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'.")

    # Set seed for reproducibility
    np.random.seed(42)

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

        # Analytical price of geometric basket option
        geo_price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)

        # Control variate adjustment
        cov = np.cov(payoffs, geo_payoffs)[0, 1]
        var_geo = np.var(geo_payoffs)
        beta = cov / var_geo

        adjusted_payoffs = payoffs - beta * (geo_payoffs - geo_price)
    else:
        adjusted_payoffs = payoffs

    # Discounted expected value and standard error
    price = np.exp(-r * T) * np.mean(adjusted_payoffs)
    stderr = np.exp(-r * T) * np.std(adjusted_payoffs) / np.sqrt(num_simulations)

    return price, stderr

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
        num_simulations = int(input("Enter number of simulations: "))
        control_variate = input("Enter control variate method (none/geometric): ")
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        if control_variate not in ['none', 'geometric']:
            raise ValueError("Control variate method must be either 'none' or 'geometric'")
        if rho < -1 or rho > 1:
            raise ValueError("Correlation must be between -1 and 1")
        
        price, stderr = arithmetic_basket_mc(S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        print(f"Standard error: {stderr:.10f}")
        print(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 