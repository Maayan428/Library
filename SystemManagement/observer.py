from abc import ABC, abstractmethod

class Observer(ABC):

    @abstractmethod
    def update(self, message):
        raise NotImplementedError("Subclasses must implement this method.")