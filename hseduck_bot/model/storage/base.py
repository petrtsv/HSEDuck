from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the db connection.
        :return: None
        """
        pass

    @abstractmethod
    def build_scheme(self) -> None:
        """
        Create necessary tables.
        :return:
        """
        pass

    @abstractmethod
    def close(self) -> None:
        pass
