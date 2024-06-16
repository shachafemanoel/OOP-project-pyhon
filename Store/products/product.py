from Store.payment_calculator import CurrencyConverter
from Store.rating import Rating
from Store.storeerror import StoreError


class Product:
    def __init__(self, name, model, description, price, quantity,rate=None):  #
        self.name = name  # שם המוצר
        self.model = model  # דגם
        self.description = description  # תיאור המוצר
        self.original_price = price
        self.price = price  # מחיר המוצר
        self.sale = 0
        self.quantity = quantity  # הכמות המוצר
        self.rate = Rating(rate) if rate is not None else Rating()
        self.currency = "₪ILS"

    def get_key_name(self):
        return self.name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def get_model_name(self):
        return self.model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def buy_product(self, many):  # הוצאת כמות מוצרים מהמלאי
        self.quantity -= many

    def update_price(self, discount):
        self.sale = discount
        self.price -= (self.original_price * float(discount / 100))

    def remove_discount(self):
        self.price = self.original_price
        self.sale = 0

    def change_quantity(self, new_quantity):  # שינוי המלאי לפי מלאי חדש
        self.quantity = new_quantity

    def get_price(self, much):  # לראות רק את המחיר
        return self.price * much

    def get_quantity(self):  # לראות רק את הכמות של המוצר
        return self.quantity

    def add_quantity(self, quantity):
        self.quantity += quantity

    def available(self, how_many):  # בדיקת זמינות של מוצר מסוים
           if how_many >self.quantity:
              return False
           else:
               return True

    def add_review(self, stars, review):
        self.rate.add_review(stars, review)

    def product_to_dict(self):
        dict = {}
        dict['product_type'] = "Product"
        dict['name'] = self.name
        dict["model"] = self.model
        dict['description'] = self.description
        dict['price'] = self.original_price
        dict['quantity'] = self.quantity
        dict['rate'] = self.rate.ratings
        return dict

    def get_price_in_user_currency(self, quantity=1):
        price = ""
        if self.sale > 0:
            price += f" Original price:{CurrencyConverter.convert(self.original_price, "₪ILS", self.currency) * quantity} {self.currency} \n-{self.sale}% Off "
        price += f"Price: {CurrencyConverter.convert(self.price, "₪ILS", self.currency) * quantity} {self.currency}"
        return price

    def product_type(self):
        return "PRODUCT"
    def __str__(self):
        return f"======================================\n Name: {self.name}\n Model: {self.model}\n Description: {self.description}\n\n {self.get_price_in_user_currency()}\n {self.rate}"
