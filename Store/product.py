
class Product:
    def __init__(self, name=None, model=None, description=None, price=None, quantity=None, rate=None):  #
        self.name = name  # שם המוצר
        self.model = model # דגם
        self.description = description  # תיאור המוצר
        self.original_price = price
        self.sale=0
        self.price = price  # מחיר המוצר
        self.quantity = quantity  # הכמות המוצר
        if rate is None:
            self.rate = []
        else:
            self.rate = rate

    def get_key_name(self):
        return self.name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
    def get_model_name(self):
        return self.model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def buy_product(self, many):  # הוצאת כמות מוצרים מהמלאי
        if self.available(many):
            self.quantity -= many
            return True
        else:
            return False

    def update_price(self, discount):
        self.sale =discount
        self.price -= (self.price * float(discount / 100))

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
        return self.quantity >= how_many
    def add_review(self,review):
        self.rate.append(review)
        return "Thank you for your opinion"


    def review(self):
        review = '=================Rating=====================\n'
        if self.rate is not None and len(self.rate)>0:
            for rate in self.rate:
                review += f"\n{rate}"

        else:
            review += 'There are no reviews yet'

        return review

    def __str__(self):
        if self.sale >0:
            return f" ======================================\n Name: {self.name}\n Model: {self.model}\n Description: {self.description}\n \nPrice:{self.original_price} -{self.sale}% Off {self.price}₪ ILS\n{self.review()}"


        else:
            return f" ======================================\n Name: {self.name}\n Model: {self.model}\n Description: {self.description}\n \n Price: {self.price}₪\n{self.review()}\n"
