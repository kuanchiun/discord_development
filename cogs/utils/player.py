def enhance_equipped_item(self, slot_name, scroll_id, protect_scroll_id=None):
    # 1. 取得裝備
    slot = self.equipment_slot.get(slot_name)
    equipment = slot.current
    if not equipment:
        return "❌ 該欄位沒有裝備"

    # 2. 取得強化卷軸
    scroll = self.item_inventory.get(scroll_id)
    if not scroll:
        return "❌ 強化卷軸不存在"

    # 3. 若需要防爆卷軸，額外取得
    protect_scroll = None
    if scroll.destroy_on_fail:
        if not protect_scroll_id:
            return "⚠️ 此卷軸有爆裝風險，請選擇是否使用防爆卷軸"
        protect_scroll = self.item_inventory.get(protect_scroll_id)
        if not protect_scroll or protect_scroll.type != "protect":
            return "❌ 防爆卷軸無效或不存在"

    # 4. 執行強化
    new_equipment = equipment.attempt_enhance(scroll, protect_scroll)

    # 5. 根據結果更新裝備或爆裝
    if new_equipment is None:
        slot.unequip()
        result = "💥 裝備爆炸！"
    else:
        slot.equip(new_equipment)
        result = "✅ 強化成功！" if new_equipment != equipment else "❌ 強化失敗，裝備未改變"

    # 6. 移除卷軸與防爆卷軸
    self.item_inventory.remove(scroll_id)
    if protect_scroll_id:
        self.item_inventory.remove(protect_scroll_id)

    # 7. 更新屬性
    self.player_attribute.recalculate()

    return result