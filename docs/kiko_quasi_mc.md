# KIKO Put Option Pricing Documentation

## Overview

The KIKO (Knock-In Knock-Out) put option is a type of barrier option that combines features of both knock-in and knock-out options. The option becomes active (knocks in) if the underlying asset price falls below a lower barrier (L) and becomes worthless (knocks out) if the price rises above an upper barrier (U).

## Model Implementation

The pricing model uses quasi-Monte Carlo simulation with Sobol sequences for variance reduction. The implementation includes:

1. **Option Pricing**
   - Quasi-Monte Carlo simulation using Sobol sequences
   - Path generation with geometric Brownian motion
   - Barrier condition checking
   - Cash rebate for knocked-out options

2. **Delta Calculation**
   - Central finite difference method
   - 1% shift in spot price
   - Separate price calculations for up and down shifts

## Parameters

- **S**: Spot price of the underlying asset
- **K**: Strike price
- **r**: Risk-free interest rate (decimal)
- **T**: Time to maturity in years
- **sigma**: Volatility of the underlying asset (decimal)
- **L**: Lower barrier (knock-in)
- **U**: Upper barrier (knock-out)
- **R**: Cash rebate (paid if option knocks out)
- **n**: Number of observation times

## Mathematical Formulation

### Path Generation
The stock price path is generated using geometric Brownian motion:
```
S(t+Δt) = S(t) * exp((r - 0.5*σ²)Δt + σ√Δt * Z)
```
where Z is a standard normal random variable generated using Sobol sequences.

### Payoff Calculation
The payoff is calculated as:
```
Payoff = R if S(t) ≥ U for any t
         max(K - S(T), 0) if S(t) ≤ L for some t and S(t) < U for all t
         0 otherwise
```

### Delta Calculation
Delta is calculated using central finite difference:
```
Δ = (V(S + h) - V(S - h)) / (2h)
```
where h = 0.01 * S and V is the option price.

## Output

The model provides:
1. Option price (with 10 decimal places)
2. Standard error of the estimate
3. Delta (if requested)
4. 95% confidence interval for the price

## Example

```python
from kiko_quasi_mc import kiko_quasi_mc

# Input parameters
S = 100.0      # Spot price
K = 100.0      # Strike price
r = 0.05       # Risk-free rate
T = 1.0        # Time to maturity
sigma = 0.2    # Volatility
L = 90.0       # Lower barrier
U = 110.0      # Upper barrier
R = 1.0        # Cash rebate
n = 252        # Number of observation times

# Calculate price and Delta
price, stderr, delta = kiko_quasi_mc(S, K, r, T, sigma, L, U, R, n, calculate_delta=True)

print(f"Option Price: {price:.10f}")
print(f"Standard Error: {stderr:.10f}")
print(f"Delta: {delta:.10f}")
print(f"95% CI: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
```

## Notes

1. The model uses 10,000 paths for simulation, which provides a good balance between accuracy and computational efficiency.
2. The Sobol sequence is scrambled to avoid potential issues with low-dimensional projections.
3. The Delta calculation uses a 1% shift in the spot price, which is a common choice for finite difference methods.
4. The model includes validation checks for:
   - Lower barrier must be less than upper barrier
   - Cash rebate must be non-negative
   - All numerical parameters must be positive

## References

1. Glasserman, P. (2004). Monte Carlo Methods in Financial Engineering. Springer.
2. Sobol, I. M. (1967). Distribution of points in a cube and approximate evaluation of integrals. USSR Computational Mathematics and Mathematical Physics, 7(4), 86-112. 