class Reporting:
    def __init__(self):
        self.revenue = 0
        self.best_sell = None
        self.sold_products = {}
        self.message = []
        self.new_update = 0
        self.sales = []




    def new_order(self, order):
            self.revenue += order.total_amount
            self.message.append(f" ֿ\n * A new order has been placed * \n Order number: {order.order_number}    total amount: {order.total_amount} ")
            self.new_update += 1

    def best_sell_product(self):
        value = list(self.sold_products.values())
        key = list(self.sold_products.keys())
        self.best_sell = key[value.index(max(value))]

        return f"\n * {self.best_sell} is the best selling product *\n"

    def sold(self):
        return [(product, amount) for product , amount in self.sold_products.items()]

    def total_revenue(self):
        return f"Total revenue of our store: {self.revenue} ₪"

    def seen(self):
        self.new_update = 0
        self.message = []



    def __str__(self):
        if self.new_update > 0:
            new = f"\n * There are {self.new_update} new updates for you *\n"
            for messe in self.message:
                new += messe
        else:
            new = "\n * There are no new notifications * "
        if self.revenue > 0 and len(self.sold_products) >0:
            return f" {new}\n \n* Reporting summery *\n Sold products: {self.sold()} \n Store revenue: {self.revenue}₪ \n {self.best_sell_product()}"
        else:
            return f"{new}\n No purchase has been made from the store yet"