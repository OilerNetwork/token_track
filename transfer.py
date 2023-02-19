class Transfer:
    def __init__(self, sender: str, recipient: str, value: int):
        self.sender = sender
        self.recipient = recipient
        self.value = value

    def __str__(self):
        return "Transfer From: {:<32} To: {:<32} Value: {:>32}]".format(self.sender, self.recipient, self.value)