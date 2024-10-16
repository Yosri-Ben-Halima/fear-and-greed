import pickle
import numpy as np
import copy
from src.utils import min_max_scale, z_score_normalize


class CryptoMarketData:
    """
    CryptoMarketData
    ================

    A class used to represent and manipulate cryptocurrency market data. Provides methods for outlier removal, data normalization, and data persistence.

    Methods
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

    def __init__(self):
        """Initializes an empty CryptoMarketData object."""
        pass

    def z_score_cleaning(self, threshold: float = 3.0):
        """
        Winsorizes outliers from all numerical columns in the DataFrame using the Z-score method.
        
        Parameters
        ----------
        threshold : float, optional
            The Z-score threshold above which data points are considered outliers 
            (default is 3.0).
        
        Returns
        -------
        self : CryptoMarketData
            Returns the object with outliers cleaned.
        """
        numerical_cols = self.historical_data.select_dtypes(include=[np.number]).columns

        for column in numerical_cols:
            # Compute the mean and standard deviation of the column
            mean_col = self.historical_data[column].mean()
            std_col = self.historical_data[column].std()

            # Calculate Z-scores
            self.historical_data[f"{column}_z_score"] = (
                self.historical_data[column] - mean_col
            ) / std_col

            # Winsorize the outliers (clamp the values within the threshold)
            self.historical_data[column] = np.where(
                self.historical_data[f"{column}_z_score"] > threshold,
                mean_col + threshold * std_col,
                np.where(
                    self.historical_data[f"{column}_z_score"] < -threshold,
                    mean_col - threshold * std_col,
                    self.historical_data[column],
                ),
            )

        # Drop the Z-score columns after winsorizing
        self.historical_data.drop(
            columns=[f"{col}_z_score" for col in numerical_cols], inplace=True
        )

        return self

    def min_max_scale(self):
        """
        Normalizes numerical columns of the DataFrame using Min-Max scaling.

        Returns
        -------
        self : CryptoMarketData
            Returns the object with scaled numerical columns.
        """
        self.historical_data[self.historical_data.columns] = min_max_scale(self.historical_data)
        return self

    def z_score_normalize(self):
        """
        Normalizes numerical columns of the DataFrame using Z-score normalization.

        Returns
        -------
        self : CryptoMarketData
            Returns the object with normalized numerical columns.
        """
        self.historical_data[self.historical_data.columns] = z_score_normalize(self.historical_data)
        return self

    def save(self, file_name: str) -> None:
        """
        Saves the current object to a pickle file.

        Parameters
        ----------
        file_name : str
            The name of the file where the object will be saved. If the file extension is 
            not '.pkl', it will automatically be appended.

        Returns
        -------
        None
        """
        if not file_name.endswith(".pkl"):
            file_name += ".pkl"
        with open(file_name, "wb") as f:
            pickle.dump(self, f)
        print(f"{str(self.__class__).split("'")[1].split('.')[-1]} object saved to {file_name}")

    @classmethod
    def load(cls, file_name: str):
        """
        Loads and returns an object from a pickle file.

        Parameters
        ----------
        file_name : str
            The name of the file from which the object will be loaded. If the file extension 
            is not '.pkl', it will automatically be appended.

        Returns
        -------
        object : CryptoMarketData
            Returns the loaded object.
        """
        if not file_name.endswith(".pkl"):
            file_name += ".pkl"
        with open(file_name, "rb") as f:
            perp_data = pickle.load(f)
        print(f"{cls.__name__} object loaded from {file_name}")
        return perp_data

    def copy(self):
        """
        Creates a deep copy of the current object.

        Returns
        -------
        copy : CryptoMarketData
            A deep copy of the current object.
        """
        return copy.deepcopy(self)
