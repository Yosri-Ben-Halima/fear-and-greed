"""
marketdata
==========

The `marketdata` package provides modules and classes for fetching, processing,
and analyzing cryptocurrency market data such as perpetuals, options, and futures.

Modules:
--------
- crypto_market_data: Contains the base class `CryptoMarketData` for general
  market data handling, including methods for data normalization and outlier detection.

- futures_data: Contains `FuturesData` class that handles futures-specific market data and includes methods
  for data fetching and manipulation specific to futures contracts.

- options_data: Contains `OptionsData` class that focuses on options-specific data processing, including volatility
  and skew analysis for the options market.

- perpetuals_data: Contains `PerpetualsData` class that manages perpetuals-specific data fetching and processing, including metrics like funding and liquidation data.

Usage:
------
The classes in these modules allow users to collect and preprocess market data
to support various analyses, including sentiment analysis (***Fear & Greed Indices***),
backtesting strategies, and volatility modeling.
"""

from .perpetuals_data import PerpetualsData
from .futures_data import FuturesData
from .options_data import OptionsData

__annotations__ = ["PerpetualsData", "OptionsData", "FuturesData"]

__all__ = ["PerpetualsData", "OptionsData", "FuturesData"]
