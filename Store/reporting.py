

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
        self.message.append(f" \n * A new order has been placed * \n Order number: {order.order_number}    total amount: {order.total_amount} ")
        self.new_update += 1

    def best_sell_product(self):
        value = list(self.sold_products.values())
        key = list(self.sold_products.keys())
        self.best_sell = key[value.index(max(value))]
        return f"* {self.best_sell}is the best selling product *\n"

    def sold(self):
        return [(product, amount) for product, amount in self.sold_products.items()]



    def seen(self):
        self.new_update = 0
        self.message = []

    def get_sales_report_string(self):
        # המרת הנתונים לרשימה של tuples
        products = list(self.sold_products.items())
        products.append(("Store revenue", self.revenue))

        # מציאת האורך המקסימלי של השם והכמות
        max_name_length = max(len(str(product[0])) for product in products)
        max_sold_length = max(len(str(product[1])) for product in products)

        # בניית המחרוזת של הטבלה
        result = []
        table_width = max_name_length + max_sold_length + 7  # 7 למרווחים ומסגרת

        result.append("Product table".center(table_width))
        result.append('-' * table_width)
        header = f"| {'Product'.ljust(max_name_length)} | {'Sold'.rjust(max_sold_length)} |"
        result.append(header)
        result.append('-' * table_width)

        for product, sold in products:
            row = f"| {product.ljust(max_name_length)} | {str(sold).rjust(max_sold_length)} |"
            result.append(row)

        result.append('-' * table_width)

        return '\n'.join(result)

    def __str__(self):
        if self.new_update > 0:
            new = f"\n * There are {self.new_update} new updates for you *\n"
            for messe in self.message:
                new += messe
        else:
            new = "\n * There are no new notifications * "
        if self.revenue > 0 and len(self.sold_products) > 0:
            return f" \n    **** Reporting summary **** {new}\n{self.best_sell_product()}\n{self.get_sales_report_string()}"
        else:
            return f"{new}\nNo purchase has been made from the store yet"

