from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from random import choice, choices
from enum import Enum
from collections import Counter

from .scroll import Scroll
from .base_item import BaseItem

######################
# EnhanceResult class
######################
class EnhanceResult(Enum):
    SUCCESS = "✅ 強化成功！"
    FAIL = "❌ 強化失敗！"
    BROKEN = "❌ 強化失敗！裝備化為一道光消失了！"

##################
# Equipment class
##################
@dataclass
class Equipment(BaseItem):
    # 共有屬性
    item_id: str        # 查表ID
    display_name: str   # 展示名稱
    rarity: str        # 稀有度
    figure_id: str      # 圖片ID
    sell_money: int     # 商店販售價格
    purchase_money: int
    # 獨特屬性
    slot: str          # 裝備部位
    scroll_number: int   # 可使用卷軸次數
    success_level: int   # 卷軸使用成功次數
    
    item_type: str
    total_point: int
    
    perference_job: Optional[str] = None  # 偏好職業
    attribute_bonus: Dict[str, int] = field(
        default_factory = dict) # 裝備屬性加成
    sockets: List[Optional[Dict[str, int]]] = field(
        default_factory = lambda: [None, None, None]) # 裝備插槽
    
    def to_dict(self) -> Dict:
        """轉換成字典

        Returns
        -------
        Dict:
            裝備字典
        """
        
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "display_name": self.display_name,
            "rarity":    self.rarity,
            "figure_id": self.figure_id,
            "sell_money": self.sell_money,
            "purchase_money": self.purchase_money,
            "slot":  self.slot,
            "perference_job": self.perference_job,
            "attribute_bonus": self.attribute_bonus,
            "scroll_number": self.scroll_number,
            "success_level": self.success_level,
            "sockets": self.sockets,
            "total_point": self.total_point
        }
        
    @classmethod
    def from_dict(cls, data) -> "Equipment":
        """將字典轉換為裝備物件

        Parameters
        ----------
        data : dict
            裝備字典

        Returns
        -------
        Equipment
            裝備物件
        """
        
        return cls(
            item_id = data.get("item_id", ""),
            item_type = data.get("item_type", ""),
            display_name = data.get("display_name", ""),
            rarity = data.get("rarity", ""),
            figure_id = data.get("figure_id", ""),
            sell_money = data.get("sell_money", 0),
            purchase_money = data.get("purchase_money", 0),
            slot = data.get("slot", ""),
            perference_job = data.get("perference_job", None),
            attribute_bonus = data.get("attribute_bonus", {}),
            scroll_number = data.get("scroll_number", ""),
            success_level = data.get("success_level", ""),
            sockets = data.get("sockets", [None, None, None]),
            total_point = data.get("total_point", 0)
        )
    
    def get_item_id(self) -> str:
        """取得物品的唯一ID

        Returns
        -------
        str
            物品ID
        """
        
        return self.item_id
    
    def get_item_type(self) -> str:
        """取得物品的物品類型

        Returns
        -------
        str
            物品ID
        """
        
        return self.item_type
    
    def get_display_name(self) -> str:
        """取得物品的顯示名稱

        Returns
        -------
        str
            物品顯示名稱
        """
        
        return self.display_name
    
    def get_description(self):
        """取得物品的說明

        Returns
        -------
        str
            物品說明
        """
        return ""
    
    def get_rarity(self) -> str:
        """取得物品的稀有度

        Returns
        -------
        str
            物品稀有度
        """
        
        return self.rarity
    
    def get_figure_id(self) -> str:
        """取得物品的圖片ID

        Returns
        -------
        str
            物品圖片ID
        """
        
        return self.figure_id
    
    def get_sell_money(self) -> int:
        """取得物品的售價

        Returns
        -------
        str
            物品售價
        """
        
        return self.sell_money
    
    def get_purchase_money(self) -> int:
        """取得物品的商店購買價

        Returns
        -------
        int
            物品商店購買價
        """
        return self.purchase_money
    
    def initialize_attribute(self) -> None:
        attributes = ["VIT", "WIS", "STR", "INT", "DEX", "AGI", "MND", "LUK"]
        
        for attr in attributes:
            self.attribute_bonus.setdefault(attr, 0)
        
        distribution = choices(attributes, k=self.total_point)
        counts = Counter(distribution)

        for attr, count in counts.items():
            self.attribute_bonus[attr] += count

        self.total_point = 0
    
    def attempt_enhance(self, 
                        scroll: "Scroll", 
                        protect_equipment: bool = False,
                        ) -> Tuple["EnhanceResult", Optional["Equipment"]]:
        """強化裝備

        Parameters
        ----------
        scroll : Scroll
            所使用的卷軸
        protect_equipment : bool, optional
            是否使用防爆卷, by default False
            
        Returns
        -------
        EnhanceResult
            強化結果
        Equipment or None
            成功即回傳強化後的裝備, 失敗則回傳None
        """
        
        # 消耗一次卷軸使用次數
        self.scroll_number -= 1
        
        # 判定強化是否成功
        success = scroll.determine_success()
        
        # 強化成功
        if success:
            return EnhanceResult.SUCCESS, self._apply_scroll_effect(scroll)
        
        # 強化失敗
        # 卷軸是否會破壞裝備
        if scroll.is_destroy_on_fail():
            # 是否使用防爆卷
            if protect_equipment:
                return EnhanceResult.FAIL, self
            # 裝備是否破壞
            if scroll.determine_destroy():
                return EnhanceResult.BROKEN, None
        
        return EnhanceResult.FAIL, self
            
    def _apply_scroll_effect(self, scroll: "Scroll") -> "Equipment":
        """強化裝備

        Parameters
        ----------
        scroll : Scroll
            所使用的卷軸
            
        Returns
        -------
        Equipment 
            強化後的裝備
        """
        
        # 產生一份新的bouns
        new_bonus = self.attribute_bonus.copy()
        
        # 執行卷軸強化
        for attr, value in scroll.effect.items():
            new_bonus[attr] = new_bonus.get(attr, 0) + value
        
        # 處理剩餘強化次數、強化成功次數
        success_level = self.success_level + 1
        
        # 存回
        self.attribute_bonus = new_bonus
        self.success_level = success_level
        
        return self
        
    def is_perference(self, job_type) -> bool:
        """裝備是否有職業偏好

        Parameters
        ----------
        job_type : str
            職業名稱

        Returns
        -------
        bool
            是否偏好
        """
        
        if job_type == self.perference_job:
            return True
        return False
        
    
    
    
    
    