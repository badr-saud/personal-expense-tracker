import pycountry

def get_currency_choices():
    return sorted([
        (currency.alpha_3, f"{currency.alpha_3} - {currency.name}")
        for currency in pycountry.currencies
    ])
