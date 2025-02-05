from pydantic import BaseModel
from typing import List, Optional


class PaymentIntentReq(BaseModel):
    user_id: int
    name: str
    price: int
    currency: str


# client secret
class PaymentIntentRes(BaseModel):
    client_secret: str


class CheckoutSessionCreateReq(BaseModel):
    lookup_key: str
    email: str
    user_id: int


class CheckoutSessionRes(BaseModel):
    checkout_session_url: str


class StripeProductReq(BaseModel):
    lookup_key: List[str]


class Reccuring(BaseModel):
    interval: str


class StripeProductRes(BaseModel):
    product_id: str
    product_name: str
    product_description: str
    lookup_key: str
    unit_amount: int
    type: str
    recurring: Optional[Reccuring]


class StripeCustomerRes(BaseModel):
    stripe_customer_id: str
