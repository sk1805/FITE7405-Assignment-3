import numpy as np
from geometric_basket import geometric_basket

def arithmetic_basket_mc(S1, S2, K, r, T, sigma1, sigma2, rho, N, control_variate='none', option_type='call'):
    """
    Calculate the price of an arithmetic basket option using Monte Carlo simulation.
    
    Parameters:
    -----------
    S1 : float
        Spot price of the first underlying asset (S1(0))
    S2 : float
        Spot price of the second underlying asset (S2(0))
    K : float
        Strike price
    r : float
        Risk-free interest rate
    T : float
        Time to maturity in years
    sigma1 : float
        Volatility of the first underlying asset
    sigma2 : float
        Volatility of the second underlying asset
    rho : float
        Correlation between the two underlying assets
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
    # Generate correlated random numbers
    Z1 = np.random.normal(0, 1, N)
    Z2 = rho * Z1 + np.sqrt(1 - rho**2) * np.random.normal(0, 1, N)
    
    # Simulate stock prices at maturity
    S1_T = S1 * np.exp((r - 0.5*sigma1**2)*T + sigma1*np.sqrt(T)*Z1)
    S2_T = S2 * np.exp((r - 0.5*sigma2**2)*T + sigma2*np.sqrt(T)*Z2)
    
    # Calculate arithmetic average
    A = 0.5 * (S1_T + S2_T)
    
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
        # Calculate geometric basket option price
        geo_price = geometric_basket(S1, S2, K, r, T, sigma1, sigma2, rho, option_type)
        
        # Calculate geometric average
        G = np.sqrt(S1_T * S2_T)
        
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
        S1 = float(input("Enter spot price of first asset: "))
        S2 = float(input("Enter spot price of second asset: "))
        K = float(input("Enter strike price: "))
        r = float(input("Enter risk-free rate (decimal): "))
        T = float(input("Enter time to maturity (years): "))
        sigma1 = float(input("Enter volatility of first asset (decimal): "))
        sigma2 = float(input("Enter volatility of second asset (decimal): "))
        rho = float(input("Enter correlation between assets (decimal): "))
        N = int(input("Enter number of simulation paths: "))
        control_variate = input("Enter control variate method (none/geometric): ").lower()
        option_type = input("Enter option type (call/put): ").lower()
        
        if option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
        if control_variate not in ['none', 'geometric']:
            raise ValueError("Control variate method must be either 'none' or 'geometric'")
        if rho < -1 or rho > 1:
            raise ValueError("Correlation must be between -1 and 1")
        
        price, stderr = arithmetic_basket_mc(S1, S2, K, r, T, sigma1, sigma2, rho, N, control_variate, option_type)
        print(f"\n{option_type.capitalize()} option price: {price:.10f}")
        print(f"Standard error: {stderr:.10f}")
        print(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 