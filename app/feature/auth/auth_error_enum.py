from enum import Enum


class AuthErrorEnum(Enum):
    wrong_email = "wrong_email"
    email_exists = "email_exists"
    wrong_password = "wrong_password"
    account_locked = "account_locked"
    account_has_sessoin = "account_has_sessoin"
    account_too_many_attempts = "account_too_many_attempts"
    could_not_validate_credentials = "could_not_validate_credentials"
