from abc import ABC, abstractmethod
class PaymentProvider(ABC):
    @abstractmethod
    def process(self):
        pass

class MoMoPayment(PaymentProvider):
        pass

p = PaymentProvider()