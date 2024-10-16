"""
utils
=====

The `utils` package provides a set of utility functions and tools to assist with data processing,
visualization, statistical testing, and date comparison for cryptocurrency market analysis.

Modules and Functions:
-----------------------
- scaling:
  - `z_score_normalize`: Applies Z-score normalization to numerical data columns.
  - `min_max_scale`: Scales numerical data columns to a range between 0 and 1 using Min-Max scaling.

- compare_date:
  - `geq`: A utility function for comparing date strings, useful for filtering time-based data.

- data_fetchers:
  - `fetch_data`: Fetches historical cryptocurrency data, including futures, options, and perpetuals, for further analysis.

- plotting:
  - `plot_series_analysis`: Visualizes the time series data to explore trends and patterns.
  - `corr_heatmap`: Generates a heatmap to visualize correlations between different market variables.
  - `pairplot`: Plots pairwise relationships between features, useful for understanding variable interactions.
  - `signal_decomp`: Decomposes a time series into its trend, seasonal, and residual components.
  - `plot_first_order_deriv`: Plots the first-order derivative of a time series to visualize its rate of change.

- stats_tests:
  - `adf_test`: Performs the Augmented Dickey-Fuller (ADF) test to check for stationarity in time series data.

Usage:
------
This package is designed to provide essential tools for data analysis, preprocessing, and visualization,
which are integral to building financial models, backtesting strategies, and understanding market sentiment.
"""

from .scaling import z_score_normalize, min_max_scale
from .compare_date import geq
from .data_fetchers import fetch_data
from .plotting import (
    plot_series_analysis,
    corr_heatmap,
    pairplot,
    signal_decomp,
    plot_first_order_deriv,
)
from .stats_tests import adf_test


__all__ = [
    "pairplot",
    "adf_test",
    "signal_decomp",
    "fetch_data",
    "plot_first_order_deriv",
    "process_options_and_pc",
    "geq",
    "plot_series_analysis",
    "corr_heatmap",
    "min_max_scale",
    "process_futures",
    "z_score_normalize",
]
