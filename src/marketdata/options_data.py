from typing import Literal
import pandas as pd
from .crypto_market_data import CryptoMarketData
from src.utils import geq

class OptionsData(CryptoMarketData):
    __type = "options"

    def __init__(
        self,
        currency: Literal["BTC", "ETH"],
        start: str,
        end: str,
    ) -> None:
        self.__currency = currency
        self.__start = start
        self.__end = end

        self.__historical_data = None
        super().__init__()

    @classmethod
    def type(cls):
        return cls.__type

    @property
    def historical_data(self):
        return self.__historical_data

    @property
    def currency(self) -> Literal["BTC", "ETH"]:
        return self.__currency
    
    @currency.setter
    def currency(self, currency: Literal["BTC", "ETH"]) -> None:
        if self.__currency == currency:
            pass
        else:
            self.__currency = currency
            pass # Implement logic

    @property
    def start(self) -> str:
        return self.__start

    @start.setter
    def start(self, start: str) -> None:
        if geq(start, self.__start):
            self.__historical_data = self.__historical_data[
                self.__historical_data.index >= start
            ]
        else:
            df = None
            self.__historical_data = pd.concat(
                [df, self.__historical_data], axis=0, ignore_index=True
            )
        self.__start = start

    @property
    def end(self) -> str:
        return self.__end

    @end.setter
    def end(self, end: str) -> None:
        if geq(self.__end, end):
            self.__historical_data = self.__historical_data[
                self.__historical_data.index <= end
            ]
        else:
            df = None
            self.__historical_data = pd.concat(
                [self.__historical_data, df], axis=0, ignore_index=True
            )
        self.__end = end