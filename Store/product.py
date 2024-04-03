class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):  #
        self.name = name  # שם המוצר
        self.description = description  # תיאור המוצר(דגם המוצר)
        self.price = price  # מחיר המוצר
        self.quantity = quantity  # הכמות המוצר

    def get_name(self):
        return self.name

    def buy_product(self, many):  # הוצאת כמות מוצרים מהמלאי
        if self.available(many):
            self.quantity -= many
            return True
        else:
            return False

    def update_price(self, new_price):  # שינוי מחיר
        self.price = new_price

    def change_quantity(self, new_quantity):  # שינוי המלאי לפי מלאי חדש
        self.quantity = new_quantity

    def get_price(self, much):  # לראות רק את המחיר
        return self.price * much

    def get_quantity(self):  # לראות רק את הכמות של המוצר
        return self.quantity

    def available(self, how_many):  # בדיקת זמינות של מוצר מסוים
        return self.quantity >= how_many

    def __str__(self):
        return f"Name: {self.name}\n{self.description}\nPrice: {self.price}₪\nQuantity: {self.quantity}"
