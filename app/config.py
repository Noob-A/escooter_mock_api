# Specify the city used for generating street addresses.
CITY = "Moscow"
FAKER_LOCALE='ru'

# Percentage chance (0-100) that a rental payment will fail.
FAILURE_CHANCE_PERCENT = 30

# List of possible failure reasons.
FAILURE_REASONS = [
    "недостаточный баланс на вашем счете",
    "техническая ошибка платежной системы",
    "лимит по расходам превышен",
    "банковская карта недействительна",
    "ошибка при верификации платежных данных"
]
