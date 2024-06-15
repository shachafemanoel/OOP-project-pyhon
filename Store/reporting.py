

class Reporting:
    def __init__(self):
        self.revenue = 0
        self.sold_products = {}
        self.best_sell = None
        self.message = {"orders":[],"products":[],"users":[]}
        self.new_update = {"orders":0,"products":0,"users":0}
        self.total_update = 0



    def new_sold(self,name,quant):
        if name is self.sold_products:
            self.sold_products[name] += quant
        else:
            self.sold_products[name] = quant

    def return_products(self, name, amount):
        if name in self.sold_products:
            self.sold_products[name] -= amount

    def new_user(self,user_type,user_full_name):
        self.message["users"].append(f" \n * A new {user_type} has joined your store * \n full name: {user_full_name} ")
        self.new_update["users"] += 1
        self.total_update += 1

    def new_order(self, order):
        self.revenue += order.total_amount
        self.message["orders"].append(f" \n * A new order has been placed * \n Order number: {order.order_number}    total amount: {order.total_amount} ")
        self.new_update["orders"] += 1
        self.total_update += 1

    def order_canceled(self, order, amount):
        self.revenue -= amount
        self.message["orders"].append(f" \n * order has been canceled * \n Order number: {order}    total amount: {amount} ")
        self.new_update["orders"] += 1
        self.total_update += 1

    def best_sell_product(self):
        """
        Return a string with the top 3 best-selling products in descending order.

        Returns:
        str: A string with the names of the top 3 best-selling products in descending order.
        """
        if len(self.sold_products) > 0:
            sorted_sold_products = sorted(self.sold_products.items(), key=lambda item: item[1], reverse=True)
            top_three = sorted_sold_products[:3]
            top_three_names = [product[0] for product in top_three]
            return ", ".join(top_three_names)
        else:
            return "No products have been sold yet."



    def get_sales_report_string(self):
        # המרת הנתונים לרשימה של tuples
        products = list(self.sold_products.items())
        products.append(("Store revenue", f"{self.revenue} ₪ILS "))

        # מציאת האורך המקסימלי של השם והכמות
        max_name_length = max(len(str(product[0])) for product in products)
        max_sold_length = max(len(str(product[1])) for product in products)

        # בניית המחרוזת של הטבלה
        result = []
        table_width = max_name_length + max_sold_length + 7  # 7 למרווחים ומסגרת
        result.append('-' * table_width)
        result.append("Product sold  table".center(table_width))
        result.append('-' * table_width)
        header = f"| {'Product'.ljust(max_name_length)} | {'Sold'.rjust(max_sold_length)} |"
        result.append(header)
        result.append('-' * table_width)

        for product, sold in products:
            row = f"| {product.ljust(max_name_length)} | {str(sold).rjust(max_sold_length)} |"
            result.append(row)

        result.append('-' * table_width)

        return '\n'.join(result)


    def repoting_do_dict(self,sales):
        self.best_sell_product()
        reporting_data = {
            'best_sell': self.best_sell,
            'sold_products': self.sold_products,
            'message': self.message,
            'new_update': self.new_update,
            "total_update": self.total_update,
            'sales': sales
        }

        return reporting_data

    def product_warning(self,quantity,name):
        self.message["products"].append(f"\n * Warning:Less than {quantity} left in stock {name} *\n")
        self.new_update["products"] += 1
        self.total_update += 1
    def __str__(self):

         return f" \n    **** Reporting summary **** \n* {self.best_sell_product()}is the best selling product *\n{self.get_sales_report_string()}"


