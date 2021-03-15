from abc import ABC, abstractmethod, abstractproperty

class   BaseDB(ABC):

    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def bootstrap(self) -> None:
        pass
