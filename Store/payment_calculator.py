class CurrencyConverter:
    exchange_rates = {
        '$USD': 3.71,
        '€EUR': 4.07,
        "₪ILS": 1.00,
    }

    @staticmethod
    def set_exchange_rates(rates):
        """
        Set the exchange rates for the currency converter.
        נותן למשתמש אופציה לעדכן את שער המטבעות
        """
        CurrencyConverter.exchange_rates = rates

    @staticmethod
    def convert(amount, from_currency, to_currency):
        """
         הפונקיה לוקחת את הסכום במטבע שרוצים להמיר ממנו מחלקת בשער המטבע הזה
         השימוש באופציה זו היא על מנת לאפשר המרה גם מדולר לשקל ולא רק משקל למטבע אחר
        """
        if from_currency not in CurrencyConverter.exchange_rates or to_currency not in CurrencyConverter.exchange_rates:
            raise ValueError("Currency not supported")

        if from_currency == to_currency:
            return amount
        if CurrencyConverter.exchange_rates[from_currency] > CurrencyConverter.exchange_rates[to_currency]:
            return int(amount * CurrencyConverter.exchange_rates[from_currency])
        if CurrencyConverter.exchange_rates[from_currency] < CurrencyConverter.exchange_rates[to_currency]:
            return int(amount / CurrencyConverter.exchange_rates[to_currency])


class InstallmentPayment:
    @staticmethod
    def calculate_installment_amount(total_amount, number_of_installments, interest_rate=0.0):
        """
        Calculate the amount to be paid per installment.
        :param total_amount: The total amount to be paid in installments.
        :param number_of_installments: The number of installments.
        :param interest_rate: The interest rate per installment period (default is 0.0).
        :return: The installment amount.
        """
        if number_of_installments == 0:
            raise ZeroDivisionError("Number of installments cannot be zero")

        if interest_rate == 0.0:
            return total_amount / number_of_installments

        rate_per_installment = interest_rate / 100
        installment_amount = (total_amount * rate_per_installment) / (
                    1 - (1 + rate_per_installment) ** -number_of_installments)
        return installment_amount
