class Reporting:
    def __init__(self):
        self.revenue = 0
        self.best_sell = None
        self.sold_products = {}


    def best_sell_product(self):
        value = list(self.sold_products.values())
        key = list(self.sold_products.keys())
        self.best_sell =  key[value.index(max(value))]

        return f"{self.best_sell} is the best selling product"

    def sold(self):
        print("Products sold on this store:")
        return [(product, amount) for product , amount in self.sold_products.items()]

    def total_revenue(self):
        return f"Total revenue of our store: {self.revenue}₪ "

    def __str__(self):
        return f"{self.sold()} \n Store revenue: {self.revenue}₪ \n {self.best_sell_product()}"