class Reporting:
    def __init__(self):
        self.revenue = 0
        self.best_sell = None
        self.sold_products = {}
        self.messege = []
        self.new_update = 0


    def best_sell_product(self):
        value = list(self.sold_products.values())
        key = list(self.sold_products.keys())
        self.best_sell = key[value.index(max(value))]

        return f"{self.best_sell} is the best selling product"

    def sold(self):
        print("Products sold on this store:")
        return [(product, amount) for product , amount in self.sold_products.items()]

    def total_revenue(self):
        return f"Total revenue of our store: {self.revenue} ₪"

    def seen(self):
        self.new_update = 0
    def update(self):
        if self.new_update>0:
            new = f"\n *There is a new {self.new_update} Updates for you*"
            for messe in range(self.new_update-1,len(self.messege)):
                new += f"\n{self.messege[messe]}"
            return  new
        else:
            return "There are no new notifications"
    def __str__(self):
        if self.revenue>0:
            return f"{self.update()} \n {self.sold()} \n Store revenue: {self.revenue}₪ \n {self.best_sell_product()}"
        else:
            return f"{self.update()}\n No purchase has been made from the store yet"