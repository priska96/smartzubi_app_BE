from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import stripe

from .schemas import (
    PaymentIntentReq,
    PaymentIntentRes,
    CheckoutSessionCreateReq,
    CheckoutSessionRes,
    StripeCustomerRes,
    StripeProductReq,
)
from ... import models
from ...envConfig import Config

stripe.api_key = Config.STRIPE_KEY


class Payment:
    # returns customer id
    def get_or_create_customer(user_id: int, db: Session):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user.stripe_customer_id:
            return user.stripe_customer_id
        customer = stripe.Customer.create(
            name=user.username,
            email=user.email,
        )
        return customer.id

    def create_client_secret(obj_in: PaymentIntentReq, db: Session):

        customer_id = Payment.get_or_create_customer(obj_in.user_id, db)
        
        intent = stripe.PaymentIntent.create(
            # To allow saving and retrieving payment methods, provide the Customer ID.
            customer=customer_id,
            amount=obj_in.price,
            currency=obj_in.currency,
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                "enabled": True,
            },
        )
        return PaymentIntentRes(client_secret=intent.client_secret)

    def create_checkout_session(obj_in: CheckoutSessionCreateReq):
        try:
            prices = stripe.Price.list(
                lookup_keys=[obj_in.lookup_key], expand=["data.product"]
            )

            success_url = (
                Config.YOUR_DOMAIN + "/login"
                if prices.data[0].recurring == None
                else Config.YOUR_DOMAIN
                + "/payment-subscription?success=true&session_id={CHECKOUT_SESSION_ID}&user_id="
                + str(obj_in.user_id)
            )
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": prices.data[0].id,
                        "quantity": 1,
                    },
                ],
                customer_email=obj_in.email,
                mode="payment" if prices.data[0].recurring == None else "subscription",
                success_url=success_url,
                cancel_url=Config.YOUR_DOMAIN + "/payment-subscription?canceled=true",
            )
            return CheckoutSessionRes(checkout_session_url=checkout_session.url)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e
            )

    def get_customer_by_session_id(session_id: str):
        session = stripe.checkout.Session.retrieve(session_id)
        customer_id = session.customer
        return StripeCustomerRes(stripe_customer_id=customer_id)

    def get_products_by_price_lookup_key(obj_in: StripeProductReq):
        try:
            prices = stripe.Price.list(
                lookup_keys=obj_in.lookup_key, expand=["data.product"]
            )
            
            products = []

            for item in prices["data"]:
                product_info = {
                    "product_id": item["product"]["id"],
                    "product_name": item["product"]["name"],
                    "product_description": item["product"]["description"],
                    "lookup_key": item["lookup_key"],
                    "unit_amount": item["unit_amount"],
                    "type": item["type"],
                    "recurring": (
                        {"interval": item["recurring"]["interval"]}
                        if item["recurring"]
                        else None
                    ),
                }
                products.append(product_info)
            return products
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e
            )
