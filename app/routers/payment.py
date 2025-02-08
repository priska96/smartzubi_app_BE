from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import stripe

from ..envConfig import Config
from ..database import get_db
from ..api_wrappers import token_required
from ..feature.auth.auth_bearer import jwt_bearer
from ..feature.payment.schemas import (
    PaymentIntentReq,
    PaymentIntentRes,
    CheckoutSessionCreateReq,
    CheckoutSessionRes,
    StripeCustomerRes,
    StripeProductReq,
    StripeProductRes,
)
from ..feature.payment.payment_api import Payment

# Create an APIRouter instance
router = APIRouter(prefix="/api/payment", tags=["payment"])

stripe.api_key = Config.STRIPE_KEY


@router.post("/create-intent", response_model=PaymentIntentRes)
@token_required
async def create_intent(
    obj_in: PaymentIntentReq,
    db: Session = Depends(get_db),
    dependencies=Depends(jwt_bearer),
):
    print("create intent", obj_in)
    return Payment.create_client_secret(obj_in, db)


@router.post("/create-checkout-session", response_model=CheckoutSessionRes)
def create_checkout_session(obj_in: CheckoutSessionCreateReq):
    return Payment.create_checkout_session(obj_in)


@router.post("/get-stripe-products", response_model=List[StripeProductRes])
async def get_products(obj_in: StripeProductReq):
    return Payment.get_products_by_price_lookup_key(obj_in)


@router.get("/get-customer/session_id/{session_id}", response_model=StripeCustomerRes)
async def get_customer_by_session_id(session_id: str):
    return Payment.get_customer_by_session_id(session_id)
