from typing import Literal
import pandas as pd
from .crypto_market_data import CryptoMarketData
from src.utils import geq, fetch_data


class OptionsData(CryptoMarketData):
    """
    OptionsData
    ===========

    A class used to represent and manipulate options market data for cryptocurrencies.

    This class inherits from `CryptoMarketData` and provides methods for fetching,
    storing, and managing options data for specified cryptocurrencies (BTC or ETH)
    over a given date range.

    Attributes
    ----------
    __type : str
        The type of market data (options), used internally for fetching the data. (class attribute)
    __currency : Literal["BTC", "ETH"]
        The cryptocurrency symbol (BTC or ETH) for which options data is to be fetched.
    __start : str
        The start date of the historical data.
    __end : str
        The end date of the historical data.
    __historical_data : pd.DataFrame
        The DataFrame containing the historical options data for the given cryptocurrency
        and date range.

    Methods
    -------
    type()
        Returns the type of market data (options).

    Properties
    ----------
    historical_data()
        Returns the fetched historical options data as a DataFrame.
    currency()
        Gets or sets the cryptocurrency symbol for the options data (BTC or ETH).
    start()
        Gets or sets the start date for the historical data.
    end()
        Gets or sets the end date for the historical data.

    Inherited Methods
    -------

    z_score_cleaning(threshold: float = 3.0)

        Winsorizes outliers from all numerical columns in the DataFrame using the Z-score method.

    min_max_scale()

        Normalizes numerical columns of the DataFrame using Min-Max scaling.

    z_score_normalize()

        Normalizes numerical columns of the DataFrame using Z-score normalization.

    save(file_name: str) -> None

        aves the current object to a pickle file.

    load(cls, file_name: str)

        Loads and returns an object from a pickle file.

    copy()

        Returns a deep copy of the current object.
    """

    __type = "options"

    def __init__(
        self,
        currency: Literal["BTC", "ETH"],
        start: str,
        end: str,
    ) -> None:
        """
        Initializes the OptionsData object by fetching the historical options data
        for the specified cryptocurrency and date range.

        Parameters
        ----------
        currency : Literal["BTC", "ETH"]
            The cryptocurrency symbol (BTC or ETH) for which to fetch the options data.
        start : str
            The start date for the historical data in 'YYYY-MM-DD' format.
        end : str
            The end date for the historical data in 'YYYY-MM-DD' format.
        """
        self.__currency = currency
        self.__start = start
        self.__end = end

        # Fetch the historical options data for the given parameters
        self.__historical_data = fetch_data(
            self.__currency, self.type(), self.__start, self.__end
        )
        super().__init__()

    @classmethod
    def type(cls):
        """
        Returns the type of market data (options).

        Returns
        -------
        str
            The type of market data, which is "options".
        """
        return cls.__type

    @property
    def historical_data(self):
        """
        Returns the historical options data as a DataFrame.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the historical options data.
        """
        return self.__historical_data

    @property
    def currency(self) -> Literal["BTC", "ETH"]:
        """
        Gets or sets the cryptocurrency symbol (BTC or ETH) for the options data.

        When setting a new currency, it will automatically refetch the data for
        the new currency within the existing start and end dates.

        Returns
        -------
        Literal["BTC", "ETH"]
            The cryptocurrency symbol (BTC or ETH) for which the options data is fetched.

        Parameters
        ----------
        currency : Literal["BTC", "ETH"]
            The new cryptocurrency symbol to fetch the data for.
        """
        return self.__currency

    @currency.setter
    def currency(self, currency: Literal["BTC", "ETH"]) -> None:
        if self.__currency == currency:
            pass
        else:
            self.__currency = currency
            # Refetch the historical data for the new currency
            self.__historical_data = fetch_data(
                self.__currency, self.type(), self.__start, self.__end
            )

    @property
    def start(self) -> str:
        """
        Gets or sets the start date for the historical options data.

        When setting a new start date, it either filters or fetches new data to
        adjust the dataset accordingly.

        Returns
        -------
        str
            The start date for the historical data in 'YYYY-MM-DD' format.

        Parameters
        ----------
        start : str
            The new start date for the historical data.
        """
        return self.__start

    @start.setter
    def start(self, start: str) -> None:
        if geq(start, self.__start):
            # Filter existing data if the new start date is greater than or equal to the current start
            self.__historical_data = self.__historical_data[
                self.__historical_data.index >= start
            ]
        else:
            # Fetch additional data if the new start date is earlier than the current start
            df = fetch_data(self.__currency, self.type(), start, self.__start)[:-1]
            self.__historical_data = pd.concat(
                [df, self.__historical_data], axis=0, ignore_index=True
            )
        self.__start = start

    @property
    def end(self) -> str:
        """
        Gets or sets the end date for the historical options data.

        When setting a new end date, it either filters or fetches new data to
        adjust the dataset accordingly.

        Returns
        -------
        str
            The end date for the historical data in 'YYYY-MM-DD' format.

        Parameters
        ----------
        end : str
            The new end date for the historical data.
        """
        return self.__end

    @end.setter
    def end(self, end: str) -> None:
        if geq(self.__end, end):
            # Filter existing data if the new end date is less than or equal to the current end
            self.__historical_data = self.__historical_data[
                self.__historical_data.index <= end
            ]
        else:
            # Fetch additional data if the new end date is later than the current end
            df = fetch_data(self.__currency, self.type(), self.__end, end)[1:]
            self.__historical_data = pd.concat(
                [self.__historical_data, df], axis=0, ignore_index=True
            )
        self.__end = end
