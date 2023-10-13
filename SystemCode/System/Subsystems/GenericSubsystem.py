from abc import ABC, abstractmethod

class GenericSubsystem(ABC):

    def getSubsystem(self):
        return self

    def periodic(self):
        pass