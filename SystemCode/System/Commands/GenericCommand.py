from abc import ABC, abstractmethod

class GenericCommand(ABC):

    def __int__(self):
        self.initialize()
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def isFinished(self):
        pass

    @abstractmethod
    def end(self, interrupted: bool):
        pass