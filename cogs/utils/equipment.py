from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from random import choice, choices
from enum import Enum

from .scroll import Scroll

######################
# EnhanceResult class
######################
class EnhanceResult(Enum):
    SUCCESS = "強化成功！"
    FAIL = "強化失敗！"
    BROKEN = "強化失敗！裝備化為一到光消失了！"

##################
# Equipment class
##################
@dataclass
class Equipment:
    item_id: str      # 查表ID
    figure_name: str   # 圖片ID
    name: str          # 展示給玩家看的
    part: str          # 裝備部位
    rarity: str        # 稀有度
    
    attribute_bonus: Dict[str, int] = field(
        default_factory = dict) # 裝備屬性加成
    
    scroll_number: int   # 可使用卷軸次數
    success_level: int   # 卷軸使用成功次數
    
    sockets: List[Optional[Dict[str, int]]] = field(
        default_factory = [None, None, None]) # 裝備插槽
    
    sell_money: int   # 商店販賣價格
    
    def attempt_enhance(self, 
                        scroll: "Scroll", 
                        protect_equipment: bool = False,
                        ) -> Tuple["EnhanceResult", Optional["Equipment"]]:
        
        """強化裝備
        
        Args:
            scroll (Scroll): 所使用強化卷軸
            protect_equipment (bool): 是否應用防爆捲
        
        Returns:
            Equipment, None: 裝備, 破壞
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
        """執行卷軸效果
        
        Args:
            scroll (Scroll): 卷軸
            
        Return:
            Equipment: 新裝備
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
        
        
        
    
    
    
    
    