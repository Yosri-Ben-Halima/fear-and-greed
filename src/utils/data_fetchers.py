from typing import Literal
import pandas as pd

from .preprocessing import process_futures, process_options_and_pc
from .mongodb_service import get_data

def fetch_futures_data(
    coin: Literal["BTC", "ETH"], start: str, end: str
) -> pd.DataFrame:
    return process_futures(get_data(coin, "futures", start, end))


def fetch_options_data(
    coin: Literal["BTC", "ETH"], start: str, end: str
) -> pd.DataFrame:
    return process_options_and_pc(
        get_data(coin, "options", start, end), get_data(coin, "pc_ratio", start, end)
    )


def fetch_perpetuals_data(
    coin: Literal["BTC", "ETH"], start: str, end: str
) -> pd.DataFrame:
    pass


def fetch_data(coin: Literal["BTC", "ETH"], type: Literal["futures", "options", "perpetuals"] , start: str, end: str) -> pd.DataFrame:
    if type == "futures":
        return fetch_futures_data(coin, start, end)
    elif type == "options":
        return fetch_options_data(coin, start, end)
    elif type == "perpetuals":
        return fetch_perpetuals_data(coin, start, end)
    else:
        raise ValueError("Invalid type. Supported types: futures, options, perpetuals")