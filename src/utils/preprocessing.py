from datetime import datetime
import re
import pandas as pd
from typing import Literal


def parse_expiry(currency):
    """Parse currency into expiry date."""
    pattern = r"(\d{1,2})([a-z]{3})(\d{2})"
    match = re.search(pattern, currency)

    if match:
        day, month_str, year_str = match.groups()
        day = int(day)
        year = int(year_str) + 2000

        month = datetime.strptime(month_str, "%b").month

        expiry_date = datetime(year, month, day).strftime("%Y-%m-%d")
        return expiry_date
    else:
        raise ValueError(f"Error parsing currency '{currency}': No match found")


def add_expiry_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add expiry column to df DataFrame."""
    df["expiry"] = df["currency"].apply(parse_expiry)
    return df


def calculate_days_to_expiry(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate days to expiry and add it to the DataFrame."""
    df["date"] = pd.to_datetime(df["date"])
    df["expiry"] = pd.to_datetime(df["expiry"])
    df["days_to_expiry"] = (df["expiry"] - df["date"]).dt.days
    return df


def calculate_annualized_basis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate annualized basis and add it to the DataFrame."""
    df["annualized_basis"] = df["basis"] * (365 / df["days_to_expiry"])
    return df


def filter(df):
    """Filter the futures DataFrame to drop inf annualized basis."""
    return df[~(df["days_to_expiry"] == 0)]


def aggregate(
    df: pd.DataFrame, type: Literal["options", "futures", "perpetuls", "pc_ratio"]
) -> pd.DataFrame:
    """Group the DataFrame."""
    if type == "futures":
        df1 = df.groupby("date").mean(numeric_only=True)[["price", "annualized_basis"]]
        df2 = df.groupby("date").sum(numeric_only=True)[["open_interest", "volume"]]
        df = pd.concat([df1, df2], axis=1)
    elif type == "options":
        df1 = df.groupby("date").mean(numeric_only=True)[
            ["price", "atm_implied_vol", "25delta_risk_reversal", "25delta_butterfly"]
        ]
        df2 = df.groupby("date").sum(numeric_only=True)[["open_interest", "volume"]]
        df = pd.concat([df1, df2], axis=1)
    elif type == "perpetuls":
        pass
    elif type == "pc_ratio":
        df = df.groupby("date").mean(numeric_only=True)[["pc_ratio"]]

    return df


def process_futures(futures: list) -> pd.DataFrame:
    """Process the futures DataFrame."""
    df = pd.DataFrame(futures).copy()
    df = add_expiry_column(df)
    df = calculate_days_to_expiry(df)
    df = calculate_annualized_basis(df)
    df = filter(df)
    df = aggregate(df, "futures")
    return df[["price", "annualized_basis", "open_interest", "volume"]]


def process_options_and_pc(options: list, pc_ratio: list) -> pd.DataFrame:
    """Process the options and P/C ratio DataFrames."""
    df1 = pd.DataFrame(options)
    df1 = aggregate(df1, "options")
    df2 = pd.DataFrame(pc_ratio)
    df2 = aggregate(df2, "pc_ratio")
    df = pd.merge(df1, df2, left_index=True, right_index=True)
    return df
