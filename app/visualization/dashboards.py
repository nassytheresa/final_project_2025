# app/visualization/dashboards.py
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone
import pandas as pd
from app.storage.mongo import get_db
from app.etl.transform import transform_data
from app.visualization.graphs import generate_all_graphs

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    [
        html.H1(
            "Cryptocurrency Market Analysis Dashboard",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": 30},
        ),
        # Market Cap Distribution
        html.Div(
            [
                html.H2("Market Cap Distribution", style={"textAlign": "center"}),
                dcc.Graph(id="market-cap-distribution"),
            ],
            style={"marginBottom": 30},
        ),
        # Price Change Analysis
        html.Div(
            [
                html.H2("Price Change Analysis", style={"textAlign": "center"}),
                dcc.Graph(id="price-change-analysis"),
            ],
            style={"marginBottom": 30},
        ),
        # Supply Utilization
        html.Div(
            [
                html.H2("Supply Utilization", style={"textAlign": "center"}),
                dcc.Graph(id="supply-utilization"),
            ],
            style={"marginBottom": 30},
        ),
        # Top Performers
        html.Div(
            [
                html.H2("Top Performers", style={"textAlign": "center"}),
                dcc.Graph(id="top-performers"),
            ],
            style={"marginBottom": 30},
        ),
        # Auto-refresh interval
        dcc.Interval(
            id="interval-component",
            interval=5 * 60 * 1000,  # 5 minutes in milliseconds
            n_intervals=0,
        ),
    ]
)


def get_latest_data() -> dict:
    """Get the latest data from MongoDB and transform it."""
    db = get_db()
    collection = db["analysis_results"]

    # Get the most recent record
    data = collection.find_one(sort=[("timestamp", -1)])

    if not data:
        return None

    return data


@app.callback(
    [
        Output("market-cap-distribution", "figure"),
        Output("price-change-analysis", "figure"),
        Output("supply-utilization", "figure"),
        Output("top-performers", "figure"),
    ],
    [Input("interval-component", "n_intervals")],
)
def update_graphs(n):
    """Update all graphs with the latest data."""
    analysis_results = get_latest_data()

    if analysis_results is None:
        # Return empty figures if no data is available
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available",
            xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        )
        return empty_fig, empty_fig, empty_fig, empty_fig

    # Generate all graphs
    graphs = generate_all_graphs(analysis_results)

    return (
        graphs["market_cap_distribution"],
        graphs["price_change_analysis"],
        graphs["supply_utilization"],
        graphs["top_performers"],
    )


def run_dashboard_server(debug: bool = False, port: int = 8080):
    """
    Run the visualization dashboard server.

    Args:
        debug: Whether to run in debug mode
        port: Port to run the dashboard on
    """
    print(f"Starting dashboard on port {port}...")
    app.run(debug=debug, port=port, host="0.0.0.0")
