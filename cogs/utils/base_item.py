from abc import ABC, abstractmethod

class BaseItem(ABC):
    @abstractmethod
    def get_item_id(self) -> str:
        """取得 item 的唯一ID"""
        pass
    
    @abstractmethod
    def get_item_type(self) -> str:
        """取得 item 的物品類型"""
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        """取得 item 的展示名稱"""
        pass
    
    @abstractmethod
    def get_sell_money(self) -> int:
        """取得 item 的商店售價"""
        pass
    
    @abstractmethod
    def get_figure_id(self) -> str:
        """取得 item 的圖片ID"""
        pass
        
    @abstractmethod
    def get_rarity(self) -> str:
        """取得 item 稀有度"""
        pass