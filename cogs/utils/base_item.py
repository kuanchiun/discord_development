from abc import ABC, abstractmethod

class BaseItem(ABC):
    @abstractmethod
    def get_item_id(self) -> str:
        """用於 inventory 的唯一識別碼"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_sell_money(self) -> int:
        pass