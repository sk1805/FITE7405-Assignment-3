# Option Pricing Calculator

A web-based option pricing calculator that implements various option pricing models including European Options (Black-Scholes), Implied Volatility, Geometric Asian, Arithmetic Asian, Geometric Basket, Arithmetic Basket, American Options, and KIKO Put Options.

## Group 30
- Abhimanyu Bhati
- Sameer Kabani

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sk1805/FITE7405-Assignment-3.git
cd FITE7405-Assignment-3
```

### 2. Create and Activate Virtual Environment

#### For Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### For macOS/Linux:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your web browser and navigate to:
```
http://localhost:8050
```

## Running Test Cases

The project includes a comprehensive test suite for all option pricing models. To run the tests:

```bash
python models/test_scripts.py
```

This will execute test cases for all models:
- Black-Scholes (European Options)
- American Binomial Options
- Arithmetic Asian Monte Carlo
- Arithmetic Basket Monte Carlo
- Geometric Asian Options
- Geometric Basket Options
- Implied Volatility
- KIKO Quasi-Monte Carlo

Test results will show:
- Input parameters used
- Calculated option prices
- Additional metrics (where applicable):
  - Standard errors
  - Confidence intervals
  - Delta values
  - Control variate comparisons

## Features

The application provides pricing calculations for:
- European Options (Black-Scholes)
- Implied Volatility
- Geometric Asian Options
- Arithmetic Asian Options (Monte Carlo)
- Geometric Basket Options
- Arithmetic Basket Options (Monte Carlo)
- American Options (Binomial)
- KIKO Put Options (Quasi-Monte Carlo)

## Usage

1. Select the desired option type from the tabs
2. Enter the required parameters:
   - Spot Price (S)
   - Strike Price (K)
   - Risk-free Rate (r)
   - Time to Maturity (T)
   - Volatility (σ)
   - Additional parameters specific to each option type
3. Click "Calculate" to get the option price and additional metrics

## Additional Information

- Monte Carlo simulations provide confidence intervals and standard errors
- American options show early exercise premiums
- KIKO options include delta calculations
- Arithmetic options support control variate methods for variance reduction

