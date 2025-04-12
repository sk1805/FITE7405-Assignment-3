import numpy as np

def american_binomial(S, K, r, T, sigma, N, option_type):
    """
    Calculate the price of an American call/put option using the binomial tree method.

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
    N : int
        Number of steps in the binomial tree
    option_type : str
        Type of option ('call' or 'put')
    """
    # Validate input parameters
    if S <= 0:
        raise ValueError("Spot price S must be positive.")
    if K <= 0:
        raise ValueError("Strike price K must be positive.")
    if r < 0:
        raise ValueError("Risk-free rate r must be non-negative.")
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility sigma must be positive.")
    if N <= 0:
        raise ValueError("Number of steps N must be positive.")
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'")

    # Binomial tree parameters
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability

    # Initialize asset prices at maturity
    asset_prices = np.zeros(N + 1)
    for i in range(N + 1):
        asset_prices[i] = S * (u ** (N - i)) * (d ** i)

    # Initialize option values at maturity
    option_values = np.zeros(N + 1)
    for i in range(N + 1):
        if option_type == 'call':
            option_values[i] = max(0, asset_prices[i] - K)
        else:
            option_values[i] = max(0, K - asset_prices[i])

    # Backward induction for American option pricing
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            option_values[i] = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])
            # Check for early exercise
            if option_type == 'call':
                option_values[i] = max(option_values[i], asset_prices[i] - K)
            else:
                option_values[i] = max(option_values[i], K - asset_prices[i])

    return option_values[0]

if __name__ == "__main__":
    try:
        S = float(input("Enter spot price: "))
        K = float(input("Enter strike price: "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        sigma = float(input("Enter volatility (decimal): "))
        n = int(input("Enter number of time steps: "))
        option_type = input("Enter option type (call/put): ").lower()
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        
        price = american_binomial(S, K, r, T, sigma, n, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 