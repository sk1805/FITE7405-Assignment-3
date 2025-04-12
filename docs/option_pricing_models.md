# Option Pricing Models Documentation

This document provides detailed information about the option pricing models implemented in this package.

## Table of Contents
1. [Black-Scholes Model](#black-scholes-model)
2. [Implied Volatility Calculator](#implied-volatility-calculator)
3. [Asian Options](#asian-options)
4. [Basket Options](#basket-options)
5. [American Options](#american-options)
6. [KIKO Options](#kiko-options)

## Black-Scholes Model

### Overview
The Black-Scholes model is a mathematical model for pricing European options. It assumes that the underlying asset follows a geometric Brownian motion with constant drift and volatility.

### Mathematical Formulation
The Black-Scholes formula for a European call option is:

\[ C = S_0 N(d_1) - Ke^{-rT}N(d_2) \]

where:
- \( d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}} \)
- \( d_2 = d_1 - \sigma\sqrt{T} \)
- \( S_0 \) = current stock price
- \( K \) = strike price
- \( r \) = risk-free interest rate
- \( T \) = time to maturity
- \( \sigma \) = volatility
- \( N() \) = cumulative standard normal distribution

### Implementation
The implementation can be found in `black_scholes.py`. It supports both call and put options.

## Implied Volatility Calculator

### Overview
The implied volatility calculator uses the Newton-Raphson method to find the volatility that makes the Black-Scholes price equal to the observed market price.

### Mathematical Formulation
The Newton-Raphson iteration is:

\[ \sigma_{n+1} = \sigma_n - \frac{C_{BS}(\sigma_n) - C_{market}}{Vega(\sigma_n)} \]

where:
- \( C_{BS} \) = Black-Scholes price
- \( C_{market} \) = observed market price
- \( Vega \) = sensitivity of option price to volatility

### Implementation
The implementation can be found in `implied_volatility.py`.

## Asian Options

### Overview
Asian options are options whose payoff depends on the average price of the underlying asset over a certain period of time.

### Types
1. **Geometric Asian Options**
   - Uses geometric average
   - Has closed-form solution
   - Implementation in `geometric_asian.py`

2. **Arithmetic Asian Options**
   - Uses arithmetic average
   - Requires Monte Carlo simulation
   - Implementation in `arithmetic_asian_mc.py`

### Mathematical Formulation
For geometric Asian options:

\[ C = e^{-rT} \left( S_0 e^{\mu T} N(d_1) - K N(d_2) \right) \]

where:
- \( \mu = (r - \sigma^2/2)(n+1)/(2n) + \sigma^2(n+1)(2n+1)/(6n^2) \)
- \( \sigma_{avg} = \sigma \sqrt{(2n+1)/(6(n+1))} \)

## Basket Options

### Overview
Basket options are options whose payoff depends on the weighted average of multiple underlying assets.

### Types
1. **Geometric Basket Options**
   - Uses geometric average
   - Has closed-form solution
   - Implementation in `geometric_basket.py`

2. **Arithmetic Basket Options**
   - Uses arithmetic average
   - Requires Monte Carlo simulation
   - Implementation in `arithmetic_basket_mc.py`

### Mathematical Formulation
For geometric basket options:

\[ C = e^{-rT} \left( B_0 e^{\mu T} N(d_1) - K N(d_2) \right) \]

where:
- \( B_0 = \sqrt{S_1 S_2} \)
- \( \mu = r - \frac{\sigma_1^2 + \sigma_2^2}{4} + \frac{\sigma_b^2}{2} \)
- \( \sigma_b = \sqrt{\sigma_1^2 + \sigma_1\sigma_2\rho + \sigma_2^2}/2 \)

## American Options

### Overview
American options can be exercised at any time before expiration. The binomial tree method is used to price these options.

### Mathematical Formulation
The binomial tree method:
1. Constructs a tree of possible stock prices
2. Calculates option values at each node
3. Uses backward induction to find the current option price

### Implementation
The implementation can be found in `american_binomial.py`.

## KIKO Options

### Overview
KIKO (Knock-In Knock-Out) options are barrier options that become active when the underlying asset price hits a certain level (knock-in) and become worthless when it hits another level (knock-out).

### Mathematical Formulation
The price is calculated using Quasi-Monte Carlo simulation:
1. Generate stock price paths
2. Check for knock-in and knock-out conditions
3. Calculate payoffs for valid paths
4. Average the discounted payoffs

### Implementation
The implementation can be found in `kiko_quasi_mc.py`.

## References
1. Black, F., & Scholes, M. (1973). The Pricing of Options and Corporate Liabilities. Journal of Political Economy, 81(3), 637-654.
2. Hull, J. C. (2018). Options, Futures, and Other Derivatives (10th ed.). Pearson.
3. Glasserman, P. (2004). Monte Carlo Methods in Financial Engineering. Springer. 