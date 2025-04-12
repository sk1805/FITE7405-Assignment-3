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

    # Set fixed seed for reproducibility
    np.random.seed(42)
    # Monte Carlo simulation logic
    payoffs = np.zeros(num_simulations)

    for i in range(num_simulations):
        # Simulate the stock price paths for both assets
        S1_path = np.zeros(n + 1)
        S2_path = np.zeros(n + 1)
        S1_path[0] = S1
        S2_path[0] = S2

        for j in range(1, n + 1):
            Z1 = np.random.normal(0, 1)
            Z2 = rho * Z1 + np.sqrt(1 - rho**2) * np.random.normal(0, 1)
            S1_path[j] = S1_path[j - 1] * np.exp((r - 0.5 * sigma1 ** 2) * (T / n) + sigma1 * np.sqrt(T / n) * Z1)
            S2_path[j] = S2_path[j - 1] * np.exp((r - 0.5 * sigma2 ** 2) * (T / n) + sigma2 * np.sqrt(T / n) * Z2)

        # Calculate the arithmetic average
        arithmetic_avg = (S1_path[-1] + S2_path[-1]) / 2

        # Calculate payoffs based on option type
        if option_type == 'call':
            payoffs[i] = max(0, arithmetic_avg - K)
        elif option_type == 'put':
            payoffs[i] = max(0, K - arithmetic_avg)
        else:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")

    # If control variate is specified, adjust the payoffs
    if control_variate == 'geometric':
        # Calculate the geometric basket option price
        geo_price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)
        geo_payoffs = np.zeros(num_simulations)

        for i in range(num_simulations):
            # Simulate the stock price paths for both assets for geometric average
            S1_path = np.zeros(n + 1)
            S2_path = np.zeros(n + 1)
            S1_path[0] = S1
            S2_path[0] = S2

            for j in range(1, n + 1):
                Z1 = np.random.normal(0, 1)
                Z2 = rho * Z1 + np.sqrt(1 - rho**2) * np.random.normal(0, 1)
                S1_path[j] = S1_path[j - 1] * np.exp((r - 0.5 * sigma1 ** 2) * (T / n) + sigma1 * np.sqrt(T / n) * Z1)
                S2_path[j] = S2_path[j - 1] * np.exp((r - 0.5 * sigma2 ** 2) * (T / n) + sigma2 * np.sqrt(T / n) * Z2)

            # Calculate the geometric average
            geometric_avg = np.sqrt(S1_path[-1] * S2_path[-1])
            geo_payoffs[i] = max(0, geometric_avg - K)

        # Calculate control variate coefficient
        cov = np.cov(payoffs, geo_payoffs)[0, 1]
        var = np.var(geo_payoffs)
        beta = cov / var

        # Adjust payoffs using control variate
        adjusted_payoffs = payoffs - beta * (geo_payoffs - geo_price)
    else:
        adjusted_payoffs = payoffs

    # Calculate option price and standard error
    price = np.mean(adjusted_payoffs) * np.exp(-r * T)
    stderr = np.std(adjusted_payoffs) * np.exp(-r * T) / np.sqrt(num_simulations)

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