# Discord RPG Game System ｜Discord RPG 遊戲系統

A personal side project to build a modular RPG framework usable in Discord bots, written in Python.  
這是一個基於興趣而開發的個人專案，目標是建立可供 Discord 機器人使用的 RPG 遊戲框架。

🚧 Project is currently under development — only core components are partially implemented.  
🚧 本專案仍在開發階段，目前僅完成部分核心模組。

---

## Development Environment ｜開發環境

- Python >= 3.12
- PyYAML == 6.0.2
- discord.py == 2.5.2

---

## 🎯 Planned Features ｜預計系統功能

- ⚔️ Battle system｜戰鬥系統  
- 📈 Match history tracking｜戰績紀錄系統  
- 🧬 Player attribute system｜玩家屬性系統  
- 🎯 Skill system｜技能系統  
- 🎒 Inventory system｜背包系統  
- 🛡️ Equipment system (enhance, upgrade, synthesis, exchange)  
  裝備系統（強化、升階、合成、兌換）  
- 📜 Scroll system｜卷軸系統  
- 💎 Potential system｜潛能系統  
- 🎁 Lottery / gacha system｜抽獎系統

---

## ✅ Implemented So Far ｜目前已完成

- 👤 Player creation, initialization, and data tracking  
  玩家建立、初始化與資料保存  
- 🧪 Equipment structure (object only, logic not yet implemented)  
  裝備物件雛形（尚未完成功能）  
- 🎰 Basic lottery functionality｜基本抽獎功能

---

## ⚠️ Not Yet Implemented ｜尚未實裝項目（非全部，僅列出部分）

* Battle System｜戰鬥系統  
    - 🔲 Not designed yet   
          完全尚未設計，後續補上

* Player System｜玩家系統
    - 🔲 Equipment attribute bonuses not yet applied to player  
          裝備屬性尚未套用至玩家能力值

    - 🔲 Player status interface not implemented  
          玩家狀態顯示介面尚未實作

* Equipment System｜裝備系統
    - ✅ ~~Equipment-slot interaction not yet connected~~ (Completed)  
          ~~裝備與裝備欄位尚未串接~~ (已完成)

    - 🔲 Integration with scroll system not done  
          尚未整合卷軸系統

    - 🔲 Integration with potential system not done  
          尚未整合潛能系統

    - 🔲 Equipment dismantling  
          裝備拆解功能尚未實作

    - 🔲 Equipment exchange  
          裝備兌換功能尚未實作  

    - 🔲 Equipment upgrading  
          裝備升階功能尚未實作

* Skill System｜技能系統
    - 🔲 Skill design in progress  
          技能設計尚未完成

    - 🔲 Skill point allocation  
          技能加點機制尚未實作

    - 🔲 Skill activation logic  
          技能觸發與運作邏輯尚未開發

* Inventory System｜背包系統
    - 🔲 Inventory slot limits for equipment  
          裝備背包尚未實作欄位上限

    - 🔲 Add multiple item types for equipment exchange/upgrade  
          尚未新增專用物品支援裝備兌換與升階功能

* Lottery System｜抽獎系統
    - 🔲 Gacha pool preview interface  
          抽獎池內容展示尚未實作

---

## **Image Disclaimer｜圖片聲明**

All program code and textual content in this repository are licensed under the Apache License 2.0.  
However, all images shown are generated using Sora (OpenAI), and are **not included in the open-source license**.  
They are for demonstration purposes only and may be subject to copyright or usage restrictions.

本專案中的所有程式碼與文字內容皆採用 Apache License 2.0 授權。  
但所展示之圖片係使用 OpenAI 的 Sora 生成，**不包含在開源授權範圍之內**，  
僅供示意與展示使用，可能受到著作權或使用條款的限制。

