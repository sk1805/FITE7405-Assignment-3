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
                    dbc.Input(id="ga-sigma", type="number", value=0.2, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="ga-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="ga-T", type="number", value=1.0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="ga-K", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Observations (n)"),
                    dbc.Input(id="ga-n", type="number", value=100, step=1),
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
                    dbc.Input(id="aa-sigma", type="number", value=0.2, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="aa-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="aa-T", type="number", value=1.0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="aa-K", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Observations (n)"),
                    dbc.Input(id="aa-n", type="number", value=100, step=1),
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
                    dbc.Label("Number of Simulations"),
                    dbc.Input(id="aa-num-simulations", type="number", value=10000, step=1000),
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
                    dbc.Input(id="gb-sigma1", type="number", value=0.2, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility 2 (σ2)"),
                    dbc.Input(id="gb-sigma2", type="number", value=0.2, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="gb-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="gb-T", type="number", value=1.0, step=0.01),
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
                    dbc.Input(id="ab-sigma1", type="number", value=0.2, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility 2 (σ2)"),
                    dbc.Input(id="ab-sigma2", type="number", value=0.2, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="ab-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="ab-T", type="number", value=1.0, step=0.01),
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
                    dbc.Label("Number of Simulations"),
                    dbc.Input(id="ab-num-simulations", type="number", value=10000, step=1000),
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
                    dbc.Label("Spot Price (S(0))"),
                    dbc.Input(id="am-S", type="number", value=100, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)"),
                    dbc.Input(id="am-K", type="number", value=100, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)"),
                    dbc.Input(id="am-r", type="number", value=0.05, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)"),
                    dbc.Input(id="am-T", type="number", value=1.0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility (σ)"),
                    dbc.Input(id="am-sigma", type="number", value=0.2, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Steps (N)"),
                    dbc.Input(id="am-N", type="number", value=100, step=1),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="am-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call"
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="am-calculate", color="primary", className="mt-3"),
            html.Div(id="am-result")
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
                    dbc.Input(id="kiko-T", type="number", value=1.0, step=0.01),
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
                    dbc.Input(id="kiko-U", type="number", value=120, step=0.01),
                ], width=6),
                dbc.Col([
                    dbc.Label("Cash Rebate (R)"),
                    dbc.Input(id="kiko-R", type="number", value=0, step=0.01),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Number of Observation Times (n)"),
                    dbc.Input(id="kiko-n", type="number", value=100, step=1),
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
    try:
        price = black_scholes(S, K, r, q, T, sigma, option_type)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Option Price: {price:.10f}")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

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
    try:
        sigma = implied_volatility(S, K, r, q, T, market_price, option_type)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Implied Volatility: {sigma:.10f}")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

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
    try:
        price = geometric_asian(S, sigma, r, T, K, n, option_type)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Option Price: {price:.10f}")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

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
    try:
        price, stderr = arithmetic_asian_mc(S, sigma, r, T, K, n, option_type, num_simulations, control_variate)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Option Price: {price:.10f}"),
            html.P(f"Standard Error: {stderr:.10f}"),
            html.P(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

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
    try:
        price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Option Price: {price:.10f}")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

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
    try:
        price, stderr = arithmetic_basket_mc(S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Option Price: {price:.10f}"),
            html.P(f"Standard Error: {stderr:.10f}"),
            html.P(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

@app.callback(
    Output("am-result", "children"),
    [Input("am-calculate", "n_clicks")],
    [
        State("am-S", "value"),
        State("am-K", "value"),
        State("am-r", "value"),
        State("am-T", "value"),
        State("am-sigma", "value"),
        State("am-N", "value"),
        State("am-option-type", "value"),
    ],
)
def calculate_american(n_clicks, S, K, r, T, sigma, N, option_type):
    if n_clicks is None:
        return ""
    try:
        price = american_binomial(S, K, r, T, sigma, N, option_type)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Option Price: {price:.10f}")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

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
    try:
        price, stderr, delta = kiko_quasi_mc(S, K, r, T, sigma, L, U, R, n, calculate_delta)
        return html.Div([
            html.H4("Results:"),
            html.P(f"Option Price: {price:.10f}"),
            html.P(f"Standard Error: {stderr:.10f}"),
            html.P(f"95% Confidence Interval: [{price-1.96*stderr:.10f}, {price+1.96*stderr:.10f}]"),
            html.P(f"Delta: {delta:.10f}")
        ])
    except Exception as e:
        return html.Div([
            html.H4("Error:"),
            html.P(str(e))
        ], className="text-danger")

if __name__ == "__main__":
    app.run_server(debug=True) 