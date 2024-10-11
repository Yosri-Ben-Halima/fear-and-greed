import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose
from typing import Literal


def plot_series_analysis(series: pd.Series) -> None:
    """
    Generates a 2x2 plot matrix for a pd.Series object with the following visualizations:
    1. Time series plot
    2. Distribution plot (Histogram and KDE)
    3. Boxplot
    4. QQ plot

    Parameters
    ----------
    series : pd.Series
        The input time series data to be analyzed.

    Returns
    -------
    None
    """

    # Set up the 2x2 subplot matrix
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Analysis of Series: {series.name}", fontsize=16)

    # 1. Time series plot (Top Left)
    axes[0, 0].plot(series.index, series.values, label="Time Series", color="b")
    axes[0, 0].set_title("Time Series Plot")
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].set_ylabel("Values")
    axes[0, 0].grid(True)

    # 2. Distribution plot (Top Right: Histogram + KDE)
    sns.histplot(series, kde=True, ax=axes[0, 1], color="g", stat="density")
    axes[0, 1].set_title("Distribution (Histogram & KDE)")
    axes[0, 1].set_xlabel("Values")
    axes[0, 1].set_ylabel("Density")
    axes[0, 1].grid(True)

    # 3. Boxplot (Bottom Left)
    sns.boxplot(x=series, ax=axes[1, 0], color="orange")
    axes[1, 0].set_title("Boxplot")
    axes[1, 0].set_xlabel("Values")
    axes[1, 0].grid(True)

    # 4. QQ plot (Bottom Right)
    stats.probplot(series, dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title("QQ Plot")
    axes[1, 1].get_lines()[1].set_color("red")  # Set the color of the QQ line
    axes[1, 1].grid(True)

    # Adjust layout for better appearance
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def plot_first_order_deriv(data: pd.Series):
    # Step 1: Compute the first derivative (rate of change)
    derivative = data.diff().dropna()

    # Step 2: Separate positive and negative values for the area plot
    positive_derivative = derivative.clip(lower=0)  # Keep only positive values
    negative_derivative = derivative.clip(upper=0)  # Keep only negative values

    # Step 3: Create subplots (2 rows, 1 column)
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Trend Component", "First Derivative"),
    )

    # Step 4: Add the line plot of the trend (subplot 1)
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data,
            mode="lines",
            name="Trend Component",
            line=dict(color="blue"),
        ),
        row=1,
        col=1,
    )

    # Step 5: Add the positive area plot (subplot 2)
    fig.add_trace(
        go.Scatter(
            x=positive_derivative.index,
            y=positive_derivative,
            mode="lines",
            fill="tozeroy",  # Fill to the x-axis
            name="Positive Derivative",
            line=dict(color="green"),
            fillcolor="rgba(0, 255, 0, 0.3)",  # Green color with transparency
        ),
        row=2,
        col=1,
    )

    # Step 6: Add the negative area plot (subplot 2)
    fig.add_trace(
        go.Scatter(
            x=negative_derivative.index,
            y=negative_derivative,
            mode="lines",
            fill="tozeroy",  # Fill to the x-axis
            name="Negative Derivative",
            line=dict(color="red"),
            fillcolor="rgba(255, 0, 0, 0.3)",  # Red color with transparency
        ),
        row=2,
        col=1,
    )


    # Step 8: Customize axis titles for both subplots
    fig.update_yaxes(title_text="Trend", row=1, col=1)
    fig.update_yaxes(title_text="First Derivative", row=2, col=1)
    # Step 7: Update layout to customize the look
    fig.update_layout(
        title="Trend Component and First Derivative",
        #xaxis_title="Time",
        yaxis_title="Derivative",
        #template='plotly_dark',
        height=600,  # Adjust height for better display
        showlegend=True,
    )

    

    # Step 9: Show the interactive plot
    fig.show()


def corr_heatmap(
    data, title, method: Literal["kendall", "pearson", "spearman"] = "pearson"
):
    """
    Generates a correlation heatmap for a given pd.DataFrame object.

    Parameters
    ----------
    data : pd.DataFrame
        The input data for which the correlation heatmap is generated.
    title : str
        The title of the plot.

    Returns
    -------
    None
    """
    corr = data.corr(method=method, numeric_only=True)
    sns.heatmap(corr, annot=True, square=True, cmap="coolwarm", fmt=".2f")
    plt.title(title)
    plt.show()


def pairplot(data, title):
    """
    Generates a pairplot for a given pd.DataFrame object with enhanced visuals.

    Parameters
    ----------
    data : pd.DataFrame
        The input data for which the pairplot is generated.
    title : str
        The title of the plot.

    Returns
    -------
    None
    """
    # Create a pairplot with a custom color palette and enhanced aesthetics
    g = sns.pairplot(
        data,
        diag_kind="kde",
        diag_kws={"alpha": 0.6},
        plot_kws={"alpha": 0.7, "s": 40, "edgecolor": "k"},
        # palette="viridis"
    )

    # Add a title to the entire plot
    g.fig.suptitle(title, fontsize=16, y=1.02)

    # Show the plot
    plt.show()


def signal_decomp(data: pd.Series, period: int = 10, return_results: bool = False):
    """
    Performs a seasonal decomposition on a given pd.Series object.

    Parameters
    ----------
    data : pd.Series
    period : int, optional
    return_results : bool, optional

    Returns
    -------
    None or pd.DataFrame
    """
    result = seasonal_decompose(
        data,
        model="additive",
        period=period,
    )

    fig = make_subplots(rows=1, cols=1)

    """fig.add_trace(
        go.Scatter(
            x=data.index,
            y=result.seasonal + result.trend,
            mode="lines",
            name="Trend + Seasonal",
        )
    )"""

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data,
            mode="lines",
            name="Original Data",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=result.trend,
            mode="lines",
            name="Trend",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=result.resid,
            mode="lines",
            name="Residuals",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=result.seasonal,
            mode="lines",
            name="Seasonal",
        )
    )

    fig.update_layout(
        title=f"Signal Decomposition of: {data.name}",
        xaxis_title="Date",
        yaxis_title=f"{data.name}",
        legend_title="Components",
        showlegend=True,
    )

    fig.show()

    if return_results:
        return result
