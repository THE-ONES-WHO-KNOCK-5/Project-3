from abc import ABC, abstractmethod


class GenericSensor(ABC):
    portVal = None

    def __int__(self, portVal):
        self.portVal = portVal

    @abstractmethod
    def getValue(self):
        pass
