# Option Pricing Models Documentation

## Overview

This project implements various option pricing models using Python. The implementation includes European, Asian, Basket, American, and KIKO options with different pricing methods.

## Running the Program

There are two ways to run the program:

1. **Command Line Interface (CLI)**
   ```bash
   python main.py
   ```
   This will launch an interactive menu where you can select and run different pricing models.

2. **Graphical User Interface (GUI)**
   ```bash
   python app.py
   ```
   This will launch a user-friendly interface with input fields for all parameters.

## Implemented Models

### 1. Black-Scholes Model
- **Purpose**: Pricing European call/put options
- **Method**: Closed-form solution
- **Features**:
  - Support for repo rate (q)
  - Implied volatility calculation
  - Error handling for invalid inputs

### 2. Asian Options
- **Geometric Asian**
  - **Method**: Closed-form solution
  - **Features**: Exact pricing for geometric average options
- **Arithmetic Asian**
  - **Method**: Monte Carlo with control variate
  - **Features**: Variance reduction using geometric Asian as control variate

### 3. Basket Options
- **Geometric Basket**
  - **Method**: Closed-form solution
  - **Features**: Exact pricing for geometric basket options
- **Arithmetic Basket**
  - **Method**: Monte Carlo with control variate
  - **Features**: 
    - Support for two assets
    - Correlation parameter (rho)
    - Variance reduction using geometric basket as control variate

### 4. American Options
- **Method**: Binomial tree
- **Features**:
  - Support for both call and put options
  - Early exercise feature
  - Configurable number of time steps

### 5. KIKO Put Options
- **Method**: Quasi-Monte Carlo with Sobol sequences
- **Features**:
  - Delta calculation using finite difference
  - Cash rebate for knocked-out options
  - Confidence intervals for price estimates

## Common Parameters

All models use the following standard parameters:
- S: Spot price
- K: Strike price
- r: Risk-free rate
- T: Time to maturity
- sigma: Volatility
- q: Repo rate (where applicable)

## Output Format

All models provide:
- Option price (with 10 decimal places)
- Standard error (for Monte Carlo methods)
- 95% confidence intervals (for Monte Carlo methods)
- Delta (for KIKO-put options)

## Example Usage

### Black-Scholes Model
```python
from black_scholes import black_scholes

# European call option
price = black_scholes(S=100, K=100, r=0.05, T=1, sigma=0.2, q=0.02, option_type='call')
print(f"Option Price: {price:.10f}")
```

### KIKO Put Option
```python
from kiko_quasi_mc import kiko_quasi_mc

# KIKO put option with Delta
price, stderr, delta = kiko_quasi_mc(
    S=100, K=100, r=0.05, T=1, sigma=0.2,
    L=90, U=110, R=1.0, n=252,
    calculate_delta=True
)
print(f"Option Price: {price:.10f}")
print(f"Delta: {delta:.10f}")
```

## Notes

1. All numerical inputs must be positive
2. Time to maturity (T) is in years
3. Rates (r, q) and volatility (sigma) should be entered as decimals
4. Monte Carlo methods use 10,000 paths for simulation
5. The binomial tree method uses configurable time steps

## References

1. Black, F., & Scholes, M. (1973). The Pricing of Options and Corporate Liabilities. Journal of Political Economy, 81(3), 637-654.
2. Glasserman, P. (2004). Monte Carlo Methods in Financial Engineering. Springer.
3. Cox, J. C., Ross, S. A., & Rubinstein, M. (1979). Option Pricing: A Simplified Approach. Journal of Financial Economics, 7(3), 229-263. 