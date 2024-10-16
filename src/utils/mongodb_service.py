from pymongo import MongoClient
from typing import Literal, Optional
from datetime import datetime
import yaml

with open("config/secrets.yml", "r") as file:
    secrets = yaml.safe_load(file)

mongo_credential = (
    secrets.get("mongodb_credential", {}).get("crypto_data", {}).get("host")
)


def parse_futures(input_data: dict) -> dict:
    # Extract values from the input data
    points = input_data.get("points", {})

    # Create the new dictionary structure
    output_data = {
        "_id": input_data["_id"],
        "date": input_data["date"],
        "currency": input_data["currency"],
        "price": points.get("0", {}).get("p"),  # Extracting price
        "open_interest": points.get("0", {}).get("oi"),  # Extracting open interest
        "volume": points.get("0", {}).get("v"),  # Extracting volume
        "basis": points.get("0", {}).get("b"),  # Extracting basis
        "yield": points.get("0", {}).get("y"),  # Extracting yield
    }

    return output_data


def parse_options(input_data: dict) -> dict:
    # Extract values from the input data
    points = input_data.get("points", {})

    # Create the new dictionary structure
    output_data = {
        "_id": input_data["_id"],
        "date": input_data["date"],
        "currency": input_data["currency"],
        "price": points.get("0", {}).get("up"),  # Extracting price
        "open_interest": points.get("0", {}).get("oi"),  # Extracting open interest
        "volume": points.get("0", {}).get("v"),  # Extracting volume
        "basis": points.get("0", {}).get("basis"),  # Extracting basis
        "atm_implied_vol": points.get("0", {}).get("atm_vol"),  # Extracting IV
        "25delta_risk_reversal": points.get("0", {}).get(
            "d_25_rr"
        ),  # Extracting 25 delta RR
        "25delta_butterfly": points.get("0", {}).get(
            "d_25_bf"
        ),  # Extracting 25 delta Butterfly
    }

    return output_data


def parse_pc(input_data: dict) -> dict:
    # Extract values from the input data
    points = input_data.get("points", {})

    # Create the new dictionary structure
    output_data = {
        "_id": input_data["_id"],
        "date": input_data["date"],
        "currency": input_data["currency"],
        "pc_ratio": points.get("0", {}).get("pc"),  # Extracting P/C Ratio
    }

    return output_data


def parse_perps(input_data: dict) -> dict:
    # Extract values from the input data
    points = input_data.get("points", {})

    # Create the new dictionary structure
    output_data = {
        "_id": input_data["_id"],
        "date": input_data["date"],
        "currency": input_data["currency"],
        "price": points.get("0", {}).get("price"),  # Extracting price
        "open_interest": points.get("0", {}).get(
            "open_interest"
        ),  # Extracting open interest
        "volume": points.get("0", {}).get("volume"),  # Extracting volume
        "funding": points.get("0", {}).get("funding"),  # Extracting basis
        "liquidations_long": points.get("0", {}).get(
            "liquidations_long"
        ),  # Extracting liquidations long side
        "liquidations_short": points.get("0", {}).get(
            "liquidations_short"
        ),  # Extracting liquidations short side
    }

    return output_data


def get_data(
    coin: Literal["BTC", "ETH"],
    type: Literal["futures", "options", "perpetuals", "pc_ratio"],
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: Optional[int] = None,
) -> list:
    client = MongoClient(mongo_credential)

    db_mapper = {
        "futures": "laevitas_futures",
        "options": "laevitas_futures",
        "perpetuals": "laevitas_futures",
        "pc_ratio": "laevitas_test",
    }
    collection_mapper = {
        "futures": "alt_future_summary",
        "options": "alt_option_summary",
        "perpetuals": "alt_summary",
        "pc_ratio": "ratio_pc",
    }

    db = client[db_mapper[type]]
    collection = db[collection_mapper[type]]

    # Create the base query for currency and hour
    query = {
        "currency": {"$regex": coin, "$options": "i"},
        "$expr": {"$eq": [{"$hour": "$date"}, 0]},
    }

    # Add date range filter if start and end dates are provided
    if start:
        query["date"] = {"$gte": datetime.fromisoformat(start)}
    if end:
        query.setdefault("date", {})["$lte"] = datetime.fromisoformat(end)

    projection = {"currency": 1, "date": 1, "points.0": 1}

    if limit is not None:
        results = collection.find(query, projection).limit(limit)
    else:
        results = collection.find(query, projection)

    if type == "futures":
        return [parse_futures(res) for res in list(results)]

    if type == "options":
        return [parse_options(res) for res in list(results)]

    if type == "pc_ratio":
        return [parse_pc(res) for res in list(results)]

    if type == "perpetuals":
        return [parse_perps(res) for res in list(results)]
