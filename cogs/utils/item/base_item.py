from abc import ABC, abstractmethod
from typing import Dict

class BaseItem(ABC):
    @abstractmethod
    def get_item_id(self) -> str:
        """取得物品的唯一ID"""
        pass
    
    @abstractmethod
    def get_item_type(self) -> str:
        """取得物品的物品類型"""
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        """取得物品的展示名稱"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """取得物品說明"""
        pass
    
    @abstractmethod
    def get_sell_money(self) -> int:
        """取得物品的商店售價"""
        pass
    
    @abstractmethod
    def get_figure_id(self) -> str:
        """取得物品的圖片ID"""
        pass
        
    @abstractmethod
    def get_rarity(self) -> str:
        """取得物品稀有度"""
        pass
    
    @abstractmethod
    def get_purchase_money(self) -> str:
        """取得物品商店購買價格"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """將物件儲存成字典"""
        pass
