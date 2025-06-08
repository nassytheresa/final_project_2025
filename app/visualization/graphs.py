import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
import pandas as pd
import os


def create_market_cap_distribution(analysis_results: Dict) -> go.Figure:
    """
    Create a market cap distribution visualization.

    Args:
        analysis_results: Dictionary containing analysis results

    Returns:
        Plotly figure object
    """
    market_cap_data = analysis_results["market_cap_analysis"]

    # Create a pie chart for market cap distribution
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Top 10 Cryptocurrencies", "Rest of Market"],
                values=[
                    market_cap_data["top_10_market_cap"],
                    market_cap_data["total_market_cap"]
                    - market_cap_data["top_10_market_cap"],
                ],
                hole=0.3,
            )
        ]
    )

    fig.update_layout(
        title="Market Cap Distribution: Top 10 vs Rest of Market",
        annotations=[
            dict(text="Market Cap", x=0.5, y=0.5, font_size=20, showarrow=False)
        ],
    )

    return fig


def create_price_change_analysis(analysis_results: Dict) -> go.Figure:
    """
    Create a price change analysis visualization.

    Args:
        analysis_results: Dictionary containing analysis results

    Returns:
        Plotly figure object
    """
    price_data = analysis_results["price_analysis"]

    # Create a bar chart for most volatile cryptocurrencies
    fig = go.Figure()

    # Add most volatile
    fig.add_trace(
        go.Bar(
            name="Most Volatile",
            x=[coin["name"] for coin in price_data["most_volatile"]],
            y=[
                coin["price_change_percentage_24h"]
                for coin in price_data["most_volatile"]
            ],
            marker_color="green",
        )
    )

    # Add least volatile
    fig.add_trace(
        go.Bar(
            name="Least Volatile",
            x=[coin["name"] for coin in price_data["least_volatile"]],
            y=[
                coin["price_change_percentage_24h"]
                for coin in price_data["least_volatile"]
            ],
            marker_color="red",
        )
    )

    fig.update_layout(
        title="24h Price Change: Most and Least Volatile Cryptocurrencies",
        xaxis_title="Cryptocurrency",
        yaxis_title="Price Change (%)",
        barmode="group",
    )

    return fig


def create_supply_utilization(analysis_results: Dict) -> go.Figure:
    """
    Create a supply utilization visualization.

    Args:
        analysis_results: Dictionary containing analysis results

    Returns:
        Plotly figure object
    """
    supply_data = analysis_results["supply_analysis"]

    # Create a horizontal bar chart for supply utilization
    fig = go.Figure()

    # Add highest utilization
    fig.add_trace(
        go.Bar(
            name="Highest Utilization",
            y=[coin["name"] for coin in supply_data["highest_utilization"]],
            x=[
                coin["supply_utilization"] * 100
                for coin in supply_data["highest_utilization"]
            ],
            orientation="h",
            marker_color="blue",
        )
    )

    # Add lowest utilization
    fig.add_trace(
        go.Bar(
            name="Lowest Utilization",
            y=[coin["name"] for coin in supply_data["lowest_utilization"]],
            x=[
                coin["supply_utilization"] * 100
                for coin in supply_data["lowest_utilization"]
            ],
            orientation="h",
            marker_color="orange",
        )
    )

    fig.update_layout(
        title="Supply Utilization: Highest and Lowest",
        xaxis_title="Supply Utilization (%)",
        yaxis_title="Cryptocurrency",
        barmode="group",
    )

    return fig


def create_top_performers(analysis_results: Dict) -> go.Figure:
    """
    Create a top performers visualization.

    Args:
        analysis_results: Dictionary containing analysis results

    Returns:
        Plotly figure object
    """
    performers = analysis_results["top_performers"]

    # Create a subplot with three bar charts
    fig = go.Figure()

    # Add market cap performers
    fig.add_trace(
        go.Bar(
            name="Market Cap",
            x=[coin["name"] for coin in performers["by_market_cap"]],
            y=[
                coin["market_cap"] / 1e9 for coin in performers["by_market_cap"]
            ],  # Convert to billions
            marker_color="purple",
        )
    )

    fig.update_layout(
        title="Top 10 Cryptocurrencies by Market Cap (Billions USD)",
        xaxis_title="Cryptocurrency",
        yaxis_title="Market Cap (Billions USD)",
        xaxis_tickangle=-45,
    )

    return fig


def generate_all_graphs(analysis_results: Dict) -> Dict[str, go.Figure]:
    """
    Generate all graphs from the analysis results.

    Args:
        analysis_results: Dictionary containing analysis results

    Returns:
        Dictionary containing all generated figures
    """
    return {
        "market_cap_distribution": create_market_cap_distribution(analysis_results),
        "price_change_analysis": create_price_change_analysis(analysis_results),
        "supply_utilization": create_supply_utilization(analysis_results),
        "top_performers": create_top_performers(analysis_results),
    }


def save_graphs_to_html(
    graphs: Dict[str, go.Figure], output_dir: str = "output/graphs"
):
    """
    Save all graphs as HTML files.

    Args:
        graphs: Dictionary of graph figures
        output_dir: Directory to save the HTML files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save each graph
    for name, fig in graphs.items():
        filename = os.path.join(output_dir, f"{name}.html")
        fig.write_html(filename)
        print(f"Saved {name} to {filename}")
