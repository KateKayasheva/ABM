class Market:
    """
    Class for  the market. Stores buy/sell books
    """
    def __init__(self):
        self.buybook = []
        self.sellbook = []

    def clear_books(self):
        """
        Reset books to an empty state
        """
        self.sellbook = []
        self.buybook = []

