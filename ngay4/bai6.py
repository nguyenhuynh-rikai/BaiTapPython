class InsufficientFundsError(Exception):
    pass

class Account:
    def __init__(self, amount):
        self.amount = amount

    def withdraw(self, amount):
        if amount > self.amount:
            raise InsufficientFundsError("Not enough money")
        self.amount -= amount
        return self.amount
acc = Account(10)

try:
    acc.withdraw(100)
except InsufficientFundsError as e:
    print(e)