from dataclasses import dataclass


@dataclass
class CustomerRegisterRequest:
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    confirm_password: str
