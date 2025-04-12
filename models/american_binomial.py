import numpy as np

def american_binomial(S, K, r, T, sigma, n, option_type='call'):
    """
    Calculate the price of an American option using the binomial tree method.
    
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
    n : int
        Number of time steps
    option_type : str, optional
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Option price
    """
    dt = T/n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1/u
    p = (np.exp(r*dt) - d)/(u - d)
    
    # Initialize stock price tree
    stock_tree = np.zeros((n+1, n+1))
    stock_tree[0, 0] = S
    
    for i in range(1, n+1):
        stock_tree[i, 0] = stock_tree[i-1, 0] * u
        for j in range(1, i+1):
            stock_tree[i, j] = stock_tree[i-1, j-1] * d
    
    # Initialize option value tree
    option_tree = np.zeros((n+1, n+1))
    
    # Calculate terminal option values
    if option_type.lower() == 'call':
        option_tree[n, :] = np.maximum(stock_tree[n, :] - K, 0)
    elif option_type.lower() == 'put':
        option_tree[n, :] = np.maximum(K - stock_tree[n, :], 0)
    else:
        raise ValueError("Option type must be either 'call' or 'put'")
    
    # Backward induction
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            # Calculate continuation value
            continuation_value = np.exp(-r*dt) * (p*option_tree[i+1, j] + (1-p)*option_tree[i+1, j+1])
            
            # Calculate exercise value
            if option_type.lower() == 'call':
                exercise_value = max(stock_tree[i, j] - K, 0)
            else:
                exercise_value = max(K - stock_tree[i, j], 0)
            
            # Take maximum of continuation and exercise values
            option_tree[i, j] = max(continuation_value, exercise_value)
    
    return option_tree[0, 0]

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