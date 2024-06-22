from Store.products.product import Product
from Store.storeerror import StoreError


class Sales:
    def __init__(self):
        """
        Initialize the Sales class with empty dictionaries for coupons, promotions, and category discounts.
        """
        self.coupons = {}
        self.promotions = {}
        self.category_discounts = {}

    def add_coupon(self, customer_id, discount):
        try:
            if 0 <= discount < 100:
                self.coupons[customer_id] = discount
            else:
                raise ValueError("Invalid discount value")
        except ValueError:
            raise StoreError.InvalidInputError("Coupon must be a digit between 0 and 99")
        except KeyError:
            raise StoreError.AuthenticationError("Client not found")

    def get_coupon_discount(self, customer_id):
        return self.coupons.get(customer_id, 0)

    def use_coupon_discount(self, customer_id):
        self.coupons.pop(customer_id, 0)

    def add_promotion(self, product_name, discount):
        """
        Add a new promotion to the store.

        Parameters:
        product_name (str): The name of the product.
        discount (float): The discount percentage (e.g., 0.10 for 10% off).
        """
        if product_name in self.promotions:
            raise ValueError("Promotion for this product already exists.")
        self.promotions[product_name] = discount

    def remove_promotion(self, product_name):
        """
        Remove a promotion from the store.

        Parameters:
        product_name (str): The name of the product to remove the promotion from.
        """
        if product_name not in self.promotions:
            raise ValueError("Promotion for this product does not exist.")
        del self.promotions[product_name]

    def update_promotion(self, product_name, new_discount):
        """
        Update the discount value of an existing promotion.

        Parameters:
        product_name (str): The name of the product to update the promotion for.
        new_discount (float): The new discount percentage.
        """
        if product_name not in self.promotions:
            raise ValueError("Promotion for this product does not exist.")
        self.promotions[product_name] = new_discount

    def add_category_discount(self, category_name, discount):
        """
        Add a new discount for a category.

        Parameters:
        category_name (str): The name of the category.
        discount (float): The discount percentage (e.g., 0.10 for 10% off).
        """
        if 0 < discount < 100:
            self.category_discounts[category_name] = discount
        else:
            raise StoreError.InvalidInputError("Invalid discount value")

    def remove_category_discount(self, category_name):
        """
        Remove a discount for a category.

        Parameters:
        category_name (str): The name of the category to remove the discount from.
        """
        if category_name not in self.category_discounts:
            raise ValueError("Discount for this category does not exist.")
        del self.category_discounts[category_name]

    def update_category_discount(self, category_name, new_discount):
        """
        Update the discount value of an existing category discount.

        Parameters:
        category_name (str): The name of the category to update the discount for.
        new_discount (float): The new discount percentage.
        """
        if category_name not in self.category_discounts:
            raise ValueError("Discount for this category does not exist.")
        self.category_discounts[category_name] = new_discount

    def get_coupon_discount(self, code):
        """
        Get the discount value of a coupon.

        Parameters:
        code (str): The coupon code.

        Returns:
        float: The discount percentage.
        """
        return self.coupons.get(code, 0)

    def get_promotion_discount(self, product_name):
        """
        Get the discount value of a promotion for a product.

        Parameters:
        product_name (str): The name of the product.

        Returns:
        float: The discount percentage.
        """
        return self.promotions.get(product_name, 0)

    def get_category_discount(self, category_name):
        """
        Get the discount value of a category.

        Parameters:
        category_name (str): The name of the category.

        Returns:
        float: The discount percentage.
        """
        return self.category_discounts.get(category_name, 0)

    def apply_coupon(self, code, price):
        """
        Apply a coupon to a given price.

        Parameters:
        code (str): The coupon code.
        price (float): The original price.

        Returns:
        float: The price after applying the coupon discount.
        """
        discount = self.get_coupon_discount(code)
        return price * (1 - discount)

    def apply_promotion(self, product_name, price):
        """
        Apply a promotion to a given price.

        Parameters:
        product_name (str): The name of the product.
        price (float): The original price.

        Returns:
        float: The price after applying the promotion discount.
        """
        discount = self.get_promotion_discount(product_name)
        return price * (1 - discount)

    def apply_category_discount(self, category_name, price):
        """
        Apply a category discount to a given price.

        Parameters:
        category_name (str): The name of the category.
        price (float): The original price.

        Returns:
        float: The price after applying the category discount.
        """
        discount = self.get_category_discount(category_name)
        return price * (1 - discount)

    def get_product_discount(self, product: Product):
        """
        Get the discount value of a product, either by promotion or category.

        Parameters:
        product (Product): The product to check the discount for.

        Returns:
        float: The highest discount percentage available for the product.
        """
        category_discount = self.get_category_discount(product.product_type().upper())
        promotion_discount = self.get_promotion_discount(product.get_key_name())
        if category_discount > promotion_discount:
            return category_discount
        else:
            return promotion_discount

    def sales_to_dict(self):
        return {
            "coupons": self.coupons,
            "promotions": self.promotions,
            "category_discounts": self.category_discounts,

        }

    def __str__(self):
        sales = "\n"
        if self.category_discounts:
            for key, value in self.category_discounts.items():
                key = "Accessories" if  key.upper() == "product".upper() else key
                sales += f"  * Sale -{value}% 🏷️  Off  {key.title()} Department!   * \n"

        return sales