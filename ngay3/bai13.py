from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def to_string(self):
        pass

s = Shape()