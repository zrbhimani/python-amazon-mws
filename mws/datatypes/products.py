"""Datatypes found in the Products API.

Docs:
https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html
"""

from mws.mws import Marketplaces
from .base import BaseDataType

__all__ = [
    "MoneyType",
    "Points",
    "PriceToEstimateFees",
    "FeesEstimateRequest",
]

CURRENCY_CODES = {
    "CAD": "Canadian dollar",
    "EUR": "European euro",
    "GBP": "Great Britain pounds",
    "INR": "Indian rupee",
    "JPY": "Japanese yen",
    "MXN": "Mexican peso",
    "RMB": "Chinese yuan",
    "USD": "United States dollar",
}


class MoneyType(BaseDataType):
    """An amount of money in a specified currency.

    Docs:
    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#MoneyType
    """

    __slots__ = ("amount", "currency_code")

    def __init__(self, amount=None, currency_code=None):
        self.amount = amount
        if currency_code is not None and currency_code not in CURRENCY_CODES:
            currency_code_str = ", ".join(CURRENCY_CODES.keys())
            raise ValueError(
                "`currency_code` must be one of the following: {}".format(
                    currency_code_str
                )
            )
        self.currency_code = currency_code


class Points(BaseDataType):
    """The number of Amazon Points offered with the purchase of an item.
    The Amazon Points program is only available in Japan.

    Docs:
    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#Points

    [python-amazon-mws]
    Construct an instance of Points by passing:
      number
        The number of Amazon Points.
        MWS expects some decimal value greater than 0,
        but we will handle the value as-is.
      monetary_value
        The monetary value of the points.
        MWS lists this as not required, but we perform a test to see if it matches
        one of the expected currency types listed in documentation.
        Raises ValueError if it does not match one of those types.
    """

    __slots__ = ("points_number", "points_monetary_value")

    def __init__(self, points_number=None, points_monetary_value=None):
        self.points_number = points_number
        if points_monetary_value is not None and not isinstance(
            points_monetary_value, MoneyType
        ):
            raise ValueError(
                "`points_monetary_value` must be an instance of `mws.datatypes.products.MoneyType`"
            )
        self.points_monetary_value = points_monetary_value


class PriceToEstimateFees(BaseDataType):
    """Price information for a product, used to estimate fees.

    Docs:
    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#PriceToEstimateFees
    """

    __slots__ = (
        "listing_price",
        "shipping",
        "points",
    )

    def __init__(self, listing_price=None, shipping=None, points=None):
        if listing_price is not None and not isinstance(listing_price, MoneyType):
            raise ValueError(
                "`listing_price` must be of an instance of `mws.datatypes.products.MoneyType`"
            )
        self.listing_price = listing_price

        if shipping is not None and not isinstance(shipping, MoneyType):
            raise ValueError(
                "`shipping` must be of an instance of `mws.datatypes.products.MoneyType`"
            )
        self.shipping = shipping

        if points is not None and not isinstance(points, Points):
            raise ValueError(
                "`points` must be of an instance of `mws.datatypes.products.Points`"
            )


class FeesEstimateRequest(BaseDataType):
    """A product, marketplace, and proposed price used to request estimated fees.

    Docs:
    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#FeesEstimateRequest
    """

    __slots__ = (
        "marketplace_id",
        "id_type",
        "id_value",
        "price_to_estimate_fees",
        "identifier",
        "is_amazon_fulfilled",
    )

    def __init__(
        self,
        marketplace=None,
        id_type=None,
        id_value=None,
        price_to_estimate_fees=None,
        identifier=None,
        is_amazon_fulfilled=None,
    ):
        """
        Identifier	A unique value that will identify this request.	Yes	Type: xs:string
        IsAmazonFulfilled
        """
        # MarketplaceId
        if marketplace in Marketplaces.__members__:
            self.marketplace_id = Marketplaces[marketplace]
        else:
            # Default to the value passed by the user.
            self.marketplace_id = marketplace

        # IdType
        if id_type not in ("ASIN", "SellerSKU"):
            raise ValueError("`id_type` must be either 'ASIN' or 'SellerSKU'")
        self.id_type = id_type

        # IdValue
        if not id_value:
            raise ValueError("`id_value` required")
        self.id_value = id_value

        # PriceToEstimateFees
        if price_to_estimate_fees is not None and not isinstance(
            price_to_estimate_fees, PriceToEstimateFees
        ):
            raise ValueError(
                "`price_to_estimate_fees` must be of an instance of `mws.datatypes.products.PriceToEstimateFees`"
            )
        self.price_to_estimate_fees = price_to_estimate_fees

        # Identifier
        self.identifier = identifier

        # IsAmazonFulfilled (boolean)
        if is_amazon_fulfilled is None:
            self.is_amazon_fulfilled = None
        else:
            self.is_amazon_fulfilled = "true" if is_amazon_fulfilled else "false"
