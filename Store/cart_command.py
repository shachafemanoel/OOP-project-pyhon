from abc import ABC, abstractmethod
from Store.cart import Cart
from Store.products.product import Product


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class AddItemCommand(Command):
    def __init__(self, cart: Cart, product: Product, quantity: int):
        self.cart = cart
        self.product = product
        self.quantity = quantity

    def execute(self):
        self.cart.add_item(self.product, self.quantity)


class RemoveItemCommand(Command):
    def __init__(self, cart: Cart, product: Product, quantity: int):
        self.cart = cart
        self.product = product
        self.quantity = quantity

    def execute(self):
        self.cart.remove_item(self.product, self.quantity)


class ChangeItemQuantityCommand(Command):
    def __init__(self, cart: Cart, product: Product, quantity: int):
        self.cart = cart
        self.product = product
        self.quantity = quantity

    def execute(self):
        self.cart.change_item_quantity(self.product, self.quantity)


class ChangeCurrencyCommand(Command):
    def __init__(self, cart: Cart, currency: str):
        self.cart = cart
        self.currency = currency

    def execute(self):
        self.cart.change_currency(self.currency)


class UseCouponCommand(Command):
    def __init__(self, cart: Cart, coupon: float):
        self.cart = cart
        self.coupon = coupon

    def execute(self):
        self.cart.use_coupon(self.coupon)


class CartInvoker:
    def __init__(self):
        self._commands = []

    def add_command(self, command: Command):
        self._commands.append(command)

    def execute_commands(self):
        for command in self._commands:
            command.execute()

    def reset_commands(self):
        self._commands.clear()

    def undo_commands(self):
        if self._commands:
            self._commands.pop()
