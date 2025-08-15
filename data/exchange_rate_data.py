#exhange_rate_data
from models.exchange_rate import ExchangeRateModel

exchange_rates = [
        # USD to others
        ExchangeRateModel(base_currency="USD", target_currency="EUR", rate=0.92),
        ExchangeRateModel(base_currency="USD", target_currency="GBP", rate=0.78),
        # EUR to others
        ExchangeRateModel(base_currency="EUR", target_currency="USD", rate=1.087),
        ExchangeRateModel(base_currency="EUR", target_currency="GBP", rate=0.85),
        # GBP to others
        ExchangeRateModel(base_currency="GBP", target_currency="USD", rate=1.28),
        ExchangeRateModel(base_currency="GBP", target_currency="EUR", rate=1.18),
    ]