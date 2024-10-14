from abc import ABC, abstractmethod
from typing import Union


class EntityABC(ABC):

    @abstractmethod
    def create(self, *args) -> Union[None, int]:
        pass

    @abstractmethod
    def find_one(self, *args) -> bool:
        pass

    @abstractmethod
    def get_all(self, *args):
        pass

    @abstractmethod
    def delete(self, *args) -> None:
        pass
