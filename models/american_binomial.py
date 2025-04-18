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
    if r < 0 or r > 1:
        raise ValueError("Risk-free rate r must be between 0 and 1.")
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

    # Terminal asset prices
    asset_prices = S * u ** np.arange(N, -1, -1) * d ** np.arange(0, N + 1)
    
    # Terminal option values
    if option_type == 'call':
        option_values = np.maximum(0, asset_prices - K)
    else:
        option_values = np.maximum(0, K - asset_prices)

    # Backward induction
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            option_value = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])
            asset_price = S * (u ** (j - i)) * (d ** i)
            if option_type == 'call':
                exercise_value = max(0, asset_price - K)
            else:
                exercise_value = max(0, K - asset_price)
            option_values[i] = max(option_value, exercise_value)
            
    return option_values[0]

if __name__ == "__main__":
    try:

        test_cases = [
            (50, 40, 0.1, 2, 0.4, 200, "put"),
            (50, 50, 0.1, 2, 0.4, 200, "put"),
            (50, 70, 0.1, 2, 0.4, 200, "put"),
        ]
        
        print("\nRunning test cases...")
        for S, K, r, T, sigma, N, option_type in test_cases:
            price = american_binomial(S, K, r, T, sigma, N, option_type)
            print(f"Results for S: {S}, K: {K}, r: {r}, T: {T}, sigma: {sigma}, N: {N}, option_type: {option_type}")
            print(f"American Binomial Option price: {price:.10f}")
            print("--------------------------------")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 