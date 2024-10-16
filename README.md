# Fear & Greed Index for Crypto Markets

## Introduction

The **Fear & Greed Index** is designed to measure the sentiment of the crypto market, focusing on **Bitcoin (BTC)** and **Ethereum (ETH)**. This project aims to create an index that reflects the overall market sentiment by analyzing data from perpetual swaps, futures, and options.

## Project Structure

```bash
fear_greed_index_project/
│
├── data/                     # Folder for raw data, preprocessed data, etc.
│   ├── raw/                  # Raw data collected from APIs - Untracked
│   └── processed/            # Cleaned and preprocessed data
│
├── notebooks/                # Jupyter notebooks for exploratory data analysis
│   ├── BTC/                      # Example notebook for EDA
│   │   └── futures_eda.ipynb
│   ├── ETH/
│   │    └── futures_eda.ipynb
│   └── FuturesFeatures.md
│
├── src/                   # Main source code for the project
│   ├── __init__.py           # Marks the src directory as a Python module
│   ├── market_data/          # Folder for data fetching and handling classes
│   │   ├── __init__.py
│   │   ├── crypto_market_data.py       # Base class for market data
│   │   ├── perpetuals_data.py          # Handles perpetuals data
│   │   ├── futures_data.py             # Handles futures data
│   │   └── options_data.py             # Handles options data
│   │
│   ├── calculators/          # Folder for classes that perform index calculations
│   │   ├── __init__.py
│   │   └── fear_greed_calculator.py    # Main class for calculating Fear & Greed Index
│   │
│   ├── backtesting/           # Folder for backtesting and validation classes
│   │   ├── __init__.py
│   │   └── backtesting.py             # Class for backtesting the index
│   │
│   └── utils/                
│       ├── compare_date.py
│       ├── data_fetchers.py
│       ├── mongodb_service.py
│       ├── plotting.py
│       ├── preprocessing.py
│       ├── scaling.py
│       ├── stats_tests.py
│       └── __init__.py          
│
├── tests/                    # Unit tests for the project
│   ├── test_perpetualsdata.py        # Tests for perpetual swaps data handling
│   ├── test_futuresdata.py           # Tests for futures data handling
│   ├── test_optionsdata.py           # Tests for options data handling
│   ├── test_feargreedcalculator.py   # Tests for Fear & Greed index calculation
│   └── test_backtesting.py           # Tests for backtesting logic
│
├── config/                   # Configuration files for APIs, environment variables, etc.
│   ├── config.yml            # Configuration file and other settings
│   └── secrets.yml           # Separate file for sensitive information (e.g., API keys, DB credentials) - Untracked
│
├── logs/                     # Log files for the system (for debugging or audit purposes) - Untracked
│   └── app.log               # Example log file
│
├── .gitignore                # Git ignore file to avoid committing unnecessary files
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies required for the project
└── setup.py                  # Script to install the project as a package

```
