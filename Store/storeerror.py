class StoreError(Exception):
    """
    Base class for exceptions in the store module.
    """
    def __init__(self, message="An error occurred in the store module"):
        """
        Initialize the error with an optional message.
        """
        self.message = message
        super().__init__(self.message)

    class InvalidInputError(Exception):
        """
        Exception raised for invalid input.
        """
        def __init__(self, message="Invalid input provided"):
            """
            Initialize the error with an optional message.
            """
            self.message = message
            super().__init__(self.message)

    class FileNotFoundError(Exception):
        """
        Exception raised when a file is not found.
        """
        def __init__(self, message="File not found"):
            """
            Initialize the error with an optional message.
            """
            self.message = message
            super().__init__(self.message)

    class ProductNotFoundError(Exception):
        """
        Exception raised when a product is not found.
        """
        def __init__(self, message="Product not found"):
            """
            Initialize the error with an optional message.
            """
            self.message = message
            super().__init__(self.message)

    class AuthenticationError(Exception):
        """
        Exception raised for authentication errors.
        """
        def __init__(self, message="Authentication failed"):
            """
            Initialize the error with an optional message.
            """
            self.message = message
            super().__init__(self.message)

    class OrderNotFoundError(Exception):
        def __init__(self, message="Order not found"):
            self.message = message
            super().__init__(self.message)

    class TooManyTriesError(Exception):
        '''
        Exceptions raised when too many tries were attempted.
        '''
        def __init__(self, message="Too many tries were attempted."):
            '''
            Initialize the error with an optional message.
            '''
            self.message = message
            super().__init__(self.message)
