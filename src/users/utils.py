import pycountry
import pytz


def get_currency_choices():
    """Returns (ISO_4217_code, 'CODE - Name') choices."""
    currencies = sorted(
        [
            (currency.alpha_3, f"{currency.alpha_3} - {currency.name}")
            for currency in pycountry.currencies
        ]
    )

    currencies = [c for c in currencies if c[0] != "ILS"]
    return currencies


def get_country_choices():
    """Returns (alpha_2_code, country_name) choices."""
    countries = sorted(
        [(country.alpha_2, country.name) for country in pycountry.countries],
        key=lambda x: x[1],
    )

    countries = [c for c in countries if c[0] != "IL"]
    return countries


def get_timezone_choices():
    """Returns (tz, tz) choices for ALL time zones."""
    timezones = [(tz, tz) for tz in pytz.all_timezones]

    timezones = [tz for tz in timezones if "Israel" not in tz[0]]
    return timezones


def get_timezones_for_country(country_code):
    """
    Returns (tz, tz) choices for a specific country.
    Falls back to UTC if no timezones are found.
    """
    return [(tz, tz) for tz in pytz.country_timezones.get(country_code, ["UTC"])]
