import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
from models.black_scholes import black_scholes
from models.implied_volatility import implied_volatility
from models.geometric_asian import geometric_asian
from models.arithmetic_asian_mc import arithmetic_asian_mc
from models.geometric_basket import geometric_basket
from models.arithmetic_basket_mc import arithmetic_basket_mc
from models.american_binomial import american_binomial
from models.kiko_quasi_mc import kiko_quasi_mc

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Model-specific tabs
tabs = [
    # Black-Scholes (European) tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))"),
                    dbc.Input(id="bs-S", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="bs-K", type="number", value=100, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="bs-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Repo Rate (q)"),
                    dbc.Input(id="bs-q", type="number", value=0.02, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="bs-T", type="number", value=1.0, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility (σ)"),
                    dbc.Input(id="bs-sigma", type="number", value=0.2, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="bs-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="bs-calculate", color="primary", className="mt-3"),
            html.Div(id="bs-result")
        ])
    ], label="European Option"),
    
    # Implied Volatility tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))"),
                    dbc.Input(id="iv-S", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="iv-K", type="number", value=100, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="iv-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Repo Rate (q)"),
                    dbc.Input(id="iv-q", type="number", value=0.02, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="iv-T", type="number", value=1.0, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Option Premium"),
                    dbc.Input(id="iv-market-price", type="number", value=10, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="iv-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="iv-calculate", color="primary", className="mt-3"),
            html.Div(id="iv-result")
        ])
    ], label="Implied Volatility"),
    
    # Geometric Asian tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))"),
                    dbc.Input(id="ga-S", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility (σ)"),
                    dbc.Input(id="ga-sigma", type="number", value=0.3, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="ga-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="ga-T", type="number", value=3.0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="ga-K", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Observations (n)"),
                    dbc.Input(id="ga-n", type="number", value=50, step=1),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="ga-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="ga-calculate", color="primary", className="mt-3"),
            html.Div(id="ga-result")
        ])
    ], label="Geometric Asian"),
    
    # Arithmetic Asian tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))"),
                    dbc.Input(id="aa-S", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility (σ)"),
                    dbc.Input(id="aa-sigma", type="number", value=0.3, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="aa-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="aa-T", type="number", value=3.0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="aa-K", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Observations (n)"),
                    dbc.Input(id="aa-n", type="number", value=50, step=1),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="aa-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call"
                    ),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Simulations (m)"),
                    dbc.Input(id="aa-num-simulations", type="number", value=100000, step=1000),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Control Variate Method"),
                    dbc.Select(
                        id="aa-control-variate",
                        options=[
                            {"label": "No Control Variate", "value": "none"},
                            {"label": "Geometric Asian", "value": "geometric"}
                        ],
                        value="none"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="aa-calculate", color="primary", className="mt-3"),
            html.Div(id="aa-result")
        ])
    ], label="Arithmetic Asian"),
    
    # Geometric Basket tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price 1 (S1(0))"),
                    dbc.Input(id="gb-S1", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Spot Price 2 (S2(0))"),
                    dbc.Input(id="gb-S2", type="number", value=100, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility 1 (σ1)"),
                    dbc.Input(id="gb-sigma1", type="number", value=0.3, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility 2 (σ2)"),
                    dbc.Input(id="gb-sigma2", type="number", value=0.3, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="gb-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="gb-T", type="number", value=3.0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="gb-K", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Correlation (ρ)"),
                    dbc.Input(id="gb-rho", type="number", value=0.5, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="gb-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="gb-calculate", color="primary", className="mt-3"),
            html.Div(id="gb-result")
        ])
    ], label="Geometric Basket"),
    
    # Arithmetic Basket tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price 1 (S1(0))"),
                    dbc.Input(id="ab-S1", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Spot Price 2 (S2(0))"),
                    dbc.Input(id="ab-S2", type="number", value=100, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility 1 (σ1)"),
                    dbc.Input(id="ab-sigma1", type="number", value=0.3, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility 2 (σ2)"),
                    dbc.Input(id="ab-sigma2", type="number", value=0.3, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="ab-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="ab-T", type="number", value=3.0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="ab-K", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Correlation (ρ)"),
                    dbc.Input(id="ab-rho", type="number", value=0.5, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="ab-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call"
                    ),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Simulations (m)"),
                    dbc.Input(id="ab-num-simulations", type="number", value=100000, step=1000),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Control Variate Method"),
                    dbc.Select(
                        id="ab-control-variate",
                        options=[
                            {"label": "No Control Variate", "value": "none"},
                            {"label": "Geometric Basket", "value": "geometric"}
                        ],
                        value="none"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="ab-calculate", color="primary", className="mt-3"),
            html.Div(id="ab-result")
        ])
    ], label="Arithmetic Basket"),
    
    # American Option tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dcc.Dropdown(
                        id='american-option-type',
                        options=[
                            {'label': 'Put', 'value': 'put'},
                            {'label': 'Call', 'value': 'call'}
                        ],
                        value='put'
                    )
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))"),
                    dbc.Input(id="american-S", type="number", value=50)
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="american-K", type="number", value=40)
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="american-r", type="number", value=0.1)
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="american-T", type="number", value=2)
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility (σ)"),
                    dbc.Input(id="american-sigma", type="number", value=0.4)
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Steps (N)"),
                    dbc.Input(id="american-N", type="number", value=200)
                ], width=6)
            ]),
            dbc.Button("Calculate", id="american-calculate", color="primary", className="mt-3"),
            html.Div(id="american-output")
        ])
    ], label="American Option"),
    
    # KIKO Put Option tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))"),
                    dbc.Input(id="kiko-S", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="kiko-K", type="number", value=100, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="kiko-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="kiko-T", type="number", value=2, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility (σ)"),
                    dbc.Input(id="kiko-sigma", type="number", value=0.2, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Lower Barrier (L)"),
                    dbc.Input(id="kiko-L", type="number", value=80, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Upper Barrier (U)"),
                    dbc.Input(id="kiko-U", type="number", value=125, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Cash Rebate (R)"),
                    dbc.Input(id="kiko-R", type="number", value=1.5, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Number of Observation Times (n)"),
                    dbc.Input(id="kiko-n", type="number", value=24, step=1),
                ], width=6),
                dbc.Col([
                    dbc.Label("Calculate Delta"),
                    dbc.Select(
                        id="kiko-calculate-delta",
                        options=[
                            {"label": "Yes", "value": "yes"},
                            {"label": "No", "value": "no"}
                        ],
                        value="yes"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="kiko-calculate", color="primary", className="mt-3"),
            html.Div(id="kiko-result")
        ])
    ], label="KIKO Put Option"),
]

# App layout
app.layout = dbc.Container([
    html.H1("Option Pricing Calculator", className="text-center my-4"),
    dbc.Tabs(tabs),
], fluid=True)

# Callbacks for each model
@app.callback(
    Output("bs-result", "children"),
    [Input("bs-calculate", "n_clicks")],
    [
        State("bs-S", "value"),
        State("bs-K", "value"),
        State("bs-r", "value"),
        State("bs-q", "value"),
        State("bs-T", "value"),
        State("bs-sigma", "value"),
        State("bs-option-type", "value"),
    ],
)
def calculate_black_scholes(n_clicks, S, K, r, q, T, sigma, option_type):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        price = black_scholes(S, K, r, q, T, sigma, option_type)
        return html.Div([
            html.H5(f"Option Price: {price:.6f}"),
        ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})

@app.callback(
    Output("iv-result", "children"),
    [Input("iv-calculate", "n_clicks")],
    [
        State("iv-S", "value"),
        State("iv-K", "value"),
        State("iv-r", "value"),
        State("iv-q", "value"),
        State("iv-T", "value"),
        State("iv-market-price", "value"),
        State("iv-option-type", "value"),
    ],
)
def calculate_implied_volatility(n_clicks, S, K, r, q, T, market_price, option_type):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        implied_vol = implied_volatility(S, K, r, q, T, market_price, option_type)
        return html.Div([
            html.H5(f"Implied Volatility: {implied_vol:.6f}"),
        ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})

@app.callback(
    Output("ga-result", "children"),
    [Input("ga-calculate", "n_clicks")],
    [
        State("ga-S", "value"),
        State("ga-sigma", "value"),
        State("ga-r", "value"),
        State("ga-T", "value"),
        State("ga-K", "value"),
        State("ga-n", "value"),
        State("ga-option-type", "value"),
    ],
)
def calculate_geometric_asian(n_clicks, S, sigma, r, T, K, n, option_type):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        price = geometric_asian(S, sigma, r, T, K, n, option_type)
        return html.Div([
            html.H5(f"Option Price: {price:.6f}"),
        ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})

@app.callback(
    Output("aa-result", "children"),
    [Input("aa-calculate", "n_clicks")],
    [
        State("aa-S", "value"),
        State("aa-sigma", "value"),
        State("aa-r", "value"),
        State("aa-T", "value"),
        State("aa-K", "value"),
        State("aa-n", "value"),
        State("aa-option-type", "value"),
        State("aa-num-simulations", "value"),
        State("aa-control-variate", "value"),
    ],
)
def calculate_arithmetic_asian(n_clicks, S, sigma, r, T, K, n, option_type, num_simulations, control_variate):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        price, stderr = arithmetic_asian_mc(S, sigma, r, T, K, n, option_type, num_simulations, control_variate)
        return html.Div([
            html.H5(f"Option Price: {price:.6f}"),
            html.H5(f"Standard Error: {stderr:.6f}"),
            html.H5(f"95% Confidence Interval: [{price-1.96*stderr:.6f}, {price+1.96*stderr:.6f}]")
        ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})

@app.callback(
    Output("gb-result", "children"),
    [Input("gb-calculate", "n_clicks")],
    [
        State("gb-S1", "value"),
        State("gb-S2", "value"),
        State("gb-sigma1", "value"),
        State("gb-sigma2", "value"),
        State("gb-r", "value"),
        State("gb-T", "value"),
        State("gb-K", "value"),
        State("gb-rho", "value"),
        State("gb-option-type", "value"),
    ],
)
def calculate_geometric_basket(n_clicks, S1, S2, sigma1, sigma2, r, T, K, rho, option_type):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)
        return html.Div([
            html.H5(f"Option Price: {price:.6f}"),
        ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})

@app.callback(
    Output("ab-result", "children"),
    [Input("ab-calculate", "n_clicks")],
    [
        State("ab-S1", "value"),
        State("ab-S2", "value"),
        State("ab-sigma1", "value"),
        State("ab-sigma2", "value"),
        State("ab-r", "value"),
        State("ab-T", "value"),
        State("ab-K", "value"),
        State("ab-rho", "value"),
        State("ab-option-type", "value"),
        State("ab-num-simulations", "value"),
        State("ab-control-variate", "value"),
    ],
)
def calculate_arithmetic_basket(n_clicks, S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        price, stderr, conf_interval = arithmetic_basket_mc(S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate)
        return html.Div([
            html.H5(f"Option Price: {price:.6f}"),
            html.H5(f"Standard Error: {stderr:.6f}"),
            html.H5(f"95% Confidence Interval: [{conf_interval[0]:.6f}, {conf_interval[1]:.6f}]")
        ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})

@app.callback(
    Output("american-output", "children"),
    [Input("american-calculate", "n_clicks")],
    [
        State("american-S", "value"),
        State("american-K", "value"),
        State("american-r", "value"),
        State("american-T", "value"),
        State("american-sigma", "value"),
        State("american-N", "value"),
        State("american-option-type", "value")
    ],
)
def calculate_american(n_clicks, S, K, r, T, sigma, N, option_type):
    if n_clicks is None:
        return ""
    
    try:
        S = float(S)
        K = float(K)
        r = float(r)
        T = float(T)
        sigma = float(sigma)
        N = int(N)
        
        # Calculate American option price
        american_price = american_binomial(S, K, r, T, sigma, N, option_type)
        
        european_price = black_scholes(S, K, r, 0, T, sigma, option_type)
        
        # Calculate early exercise premium
        early_exercise_premium = american_price - european_price
        
        return html.Div([
            html.H5(f"Option Price: {american_price:.6f}"),
            html.H5(f"Early Exercise Premium: {early_exercise_premium:.6f}"),
            html.H5(f"European {option_type.capitalize()} Price: {european_price:.6f}")
        ])
        
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.callback(
    Output("kiko-result", "children"),
    [Input("kiko-calculate", "n_clicks")],
    [
        State("kiko-S", "value"),
        State("kiko-K", "value"),
        State("kiko-r", "value"),
        State("kiko-T", "value"),
        State("kiko-sigma", "value"),
        State("kiko-L", "value"),
        State("kiko-U", "value"),
        State("kiko-R", "value"),
        State("kiko-n", "value"),
        State("kiko-calculate-delta", "value"),
    ],
)
def calculate_kiko(n_clicks, S, K, r, T, sigma, L, U, R, n, calculate_delta):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        calculate_delta = calculate_delta == "yes"
        result = kiko_quasi_mc(S, K, r, T, sigma, L, U, R, n, calculate_delta)
        if calculate_delta:
            price, stderr, conf_interval, delta = result
            return html.Div([
                html.H5(f"Option Price: {price:.6f}"),
                html.H5(f"Standard Error: {stderr:.6f}"),
                html.H5(f"95% Confidence Interval: [{conf_interval[0]:.6f}, {conf_interval[1]:.6f}]"),
                html.H5(f"Delta: {delta:.6f}"),
            ])
        else:
            price, stderr, conf_interval = result
            return html.Div([
                html.H5(f"Option Price: {price:.6f}"),
                html.H5(f"Standard Error: {stderr:.6f}"),
                html.H5(f"95% Confidence Interval: [{conf_interval[0]:.6f}, {conf_interval[1]:.6f}]"),
            ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})

if __name__ == "__main__":
    app.run_server(debug=True) 