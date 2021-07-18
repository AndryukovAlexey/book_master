from dataclasses import dataclass

from data import config

@dataclass
class Item:
    title: str
    description: str
    currency: str
    prices: list
    start_parameter: str
    provider_data = None
    photo_url: str = None
    photo_height: int = 780
    photo_width: int = 780
    need_name: bool = False
    need_phone_number: bool = False
    need_shipping_address: bool = False
    is_flexible: bool = True

    provider_token: str = config.PROVIDER_TOKEN

    def generate_invoice(self):
        return self.__dict__
