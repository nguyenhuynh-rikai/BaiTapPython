import abc
from abc import abstractmethod


class PaymentProvider(abc.ABC):
    @abstractmethod
    def process(self):
        pass

class PaypalPayment(PaymentProvider):
    pass

pp = PaypalPayment()