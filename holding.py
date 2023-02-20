import addresses
import address_comments

class Holding:
    def __init__(self, address: str):
        self._inflows = 0
        self._outflows = 0
        self._bought = 0
        self._sold = 0
        self._address = address
        self._name = addresses.lookup.get(address, address_comments.lookup.get(address, "unknown"))

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def address(self):
        return self._address

    @property
    def inflows(self):
        return self._inflows

    @inflows.setter
    def inflows(self, value):
        self._inflows = value

    @property
    def outflows(self):
        return self._outflows

    @outflows.setter
    def outflows(self, value):
        self._outflows = value

    @property
    def sold(self):
        return self._sold
    
    @sold.setter
    def sold(self, value):
        self._sold = value

    @property
    def bought(self):
        return self._bought
    
    @bought.setter
    def bought(self, value):
        self._bought = value

    @property
    def balance(self):
        return self._inflows - self._outflows

    def __str__(self):
        return "Holding [Name: {:<30} Address: {:<32} In: {:>28} Out: {:>28} Bought: {:>28} Sold: {:>28} Balance: {:>28}]".format(self.name, self.address, str(self._inflows), str(self._outflows), str(self._bought), str(self._sold), str(self.balance))
