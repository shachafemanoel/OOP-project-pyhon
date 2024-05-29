import pandas as pd

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
        return f"\n * {self.best_sell} is the best selling product *\n"

    def sold(self):
        return [(product, amount) for product, amount in self.sold_products.items()]

    def total_revenue(self):
        return f"Total revenue of our store: {self.revenue} ₪"

    def seen(self):
        self.new_update = 0
        self.message = []

    def get_sales_report_string(self):
        # המרת הנתונים ל-DataFrame
        df = pd.DataFrame(list(self.sold_products.items()), columns=['Product', 'Sold'])
        # מיון הטבלה לפי הערך של Sold מהגדול לקטן
        df = df.sort_values(by='Sold', ascending=False)
        # הוספת שורת Store revenue
        store_revenue_df = pd.DataFrame([{'Product': 'Store revenue', 'Sold': self.revenue}])
        df = pd.concat([df, store_revenue_df], ignore_index=True)

        # יצירת מחרוזת הטבלה עם מסגרת מסביב
        table_str = df.to_string(index=False, justify='center')
        lines = table_str.split('\n')
        width = len(lines[0])

        # בניית מחרוזת התוצאה
        result = []
        result.append("Product table".center(width))
        result.append('-' * width)

        # הוספת השורות עם מסגרת
        for line in lines:
            result.append(f'| {line} {""*width}|')

        # הוספת תחתית הטבלה
        result.append('-' * width)

        return '\n'.join(result)

    def __str__(self):
        if self.new_update > 0:
            new = f"\n * There are {self.new_update} new updates for you *\n"
            for messe in self.message:
                new += messe
        else:
            new = "\n * There are no new notifications * "
        if self.revenue > 0 and len(self.sold_products) > 0:
            return f"{new}\n\n* Reporting summary *\n{self.best_sell_product()}\n{self.get_sales_report_string()}"
        else:
            return f"{new}\nNo purchase has been made from the store yet"

