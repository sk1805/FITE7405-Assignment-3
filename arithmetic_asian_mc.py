import numpy as np
from geometric_asian import geometric_asian

def arithmetic_asian_mc(S, K, r, T, sigma, n, N, control_variate='none', option_type='call'):
    """
    Calculate the price of an arithmetic Asian option using Monte Carlo simulation.
    
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
        Number of observation times
    N : int
        Number of simulation paths
    control_variate : str, optional
        Control variate method ('none' or 'geometric')
    option_type : str, optional
        Type of option ('call' or 'put')
    
    Returns:
    --------
    tuple
        (Option price, Standard error)
    """
    dt = T/n
    drift = (r - 0.5*sigma**2)*dt
    vol = sigma*np.sqrt(dt)
    
    # Generate random numbers
    Z = np.random.normal(0, 1, (N, n))
    
    # Simulate stock paths
    S_paths = np.zeros((N, n+1))
    S_paths[:, 0] = S
    
    for i in range(n):
        S_paths[:, i+1] = S_paths[:, i] * np.exp(drift + vol*Z[:, i])
    
    # Calculate arithmetic averages
    A = np.mean(S_paths[:, 1:], axis=1)
    
    # Calculate payoffs
    if option_type.lower() == 'call':
        payoffs = np.maximum(A - K, 0)
    elif option_type.lower() == 'put':
        payoffs = np.maximum(K - A, 0)
    else:
        raise ValueError("Option type must be either 'call' or 'put'")
    
    # Calculate option price without control variate
    price = np.exp(-r*T) * np.mean(payoffs)
    stderr = np.exp(-r*T) * np.std(payoffs) / np.sqrt(N)
    
    if control_variate.lower() == 'geometric':
        # Calculate geometric Asian option price
        geo_price = geometric_asian(S, K, r, T, sigma, n, option_type)
        
        # Calculate geometric averages
        G = np.exp(np.mean(np.log(S_paths[:, 1:]), axis=1))
        
        # Calculate geometric payoffs
        if option_type.lower() == 'call':
            geo_payoffs = np.maximum(G - K, 0)
        else:
            geo_payoffs = np.maximum(K - G, 0)
        
        # Calculate control variate coefficient
        cov = np.cov(payoffs, geo_payoffs)[0, 1]
        var = np.var(geo_payoffs)
        beta = cov / var
        
        # Apply control variate
        cv_payoffs = payoffs - beta * (geo_payoffs - np.exp(r*T)*geo_price)
        price = np.exp(-r*T) * np.mean(cv_payoffs)
        stderr = np.exp(-r*T) * np.std(cv_payoffs) / np.sqrt(N)
    
    return price, stderr

if __name__ == "__main__":
    try:
        S = float(input("Enter spot price: "))
        K = float(input("Enter strike price: "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        sigma = float(input("Enter volatility (decimal): "))
        n = int(input("Enter number of observation times: "))
        N = int(input("Enter number of simulation paths: "))
        control_variate = input("Enter control variate method (none/geometric): ").lower()
        option_type = input("Enter option type (call/put): ").lower()
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        if control_variate not in ['none', 'geometric']:
            raise ValueError("Control variate method must be either 'none' or 'geometric'")
        
        price, stderr = arithmetic_asian_mc(S, K, r, T, sigma, n, N, control_variate, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        print(f"Standard error: {stderr:.10f}")
        print(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 