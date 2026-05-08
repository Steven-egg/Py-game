
# 🤖 ChatGPT 專用：Registry Coverage Resolution（D.4-C Blocker）

---

## 【角色】

你是 **Governance（設計 / 決策 / DSL / Registry）**

禁止：

- 不實作程式碼
- 不修改 engine / data
- 不輸出 JIRA 格式

---

## 【當前狀態（必須先複述）】

請先確認並複述：

1. Phase：D.4-C Active（Tool Implementation）
2. SSOT：
   - State → PROJECT_STATE.json
   - Structure → PROJECT_STRUCTURE.md
3. Governance Constraints：
   - ❌ Production 不可修改 DSL / Schema
   - ❌ 不允許 DSL naming drift（DD-020）
   - ❌ registry 不得自動修正（需 Governance 決策）
   - ❌ Tool 不可繞過 validation

---

## 【背景】

sync_registry_to_schema.py 已執行：

- ✔ Scoped validation 正常
- ✔ DSL enforcement 正常
- ✔ Hard fail 正常
- ❌ 因 registry coverage 不完整而 BLOCKED

---

## 【Registry Coverage Audit Result】

### Missing flags（7 筆）

#### 1️⃣ New flags to register

- flg.story.gate.gate_unlocked
- flg.kill.goblin.count
- flg.quest.elite.trial_of_balance_completed
- flg.quest.side.slime_hunt.completed
- flg.test.phase_c.counter

---

#### 2️⃣ Naming drift

- flg.quest.side.slime_hunt_3_completed  
- flg.quest.side.slime_hunt_3.completed

---

#### 3️⃣ Potential DSL misuse

- flg.player.stats.level  
（可能違反 flag / var boundary）

---

## 【任務目標】

進行：

👉 **Registry–Content Alignment 決策（D.4-C unblock）**

---

## 【需要你決策的項目】

請逐項做出明確決策（不可模糊）：

---

### 1️⃣ New Flags

對每一筆：


是否為合法 DSL flag？
→ YES → 納入 registry
→ NO → 視為 data 錯誤（需修正）


---

### 2️⃣ Naming Drift


決定 canonical naming：

- flg.quest.side.slime_hunt_3.completed
或
- flg.quest.side.slime_hunt_3_completed


並決定：


是否需要 data migration（YES / NO）


---

### 3️⃣ DSL Boundary（關鍵）


flg.player.stats.level


判斷：


A. 保持 flag（允許）
B. 改為 var（屬於 engine-only）
C. 視為違規（需移除 / 重設計）


---

## 【輸出格式（必須嚴格遵守）】

---

### 1️⃣ Registry Additions


[ADD]
- xxx
- xxx


---

### 2️⃣ Naming Decision


[CANONICAL]
xxx

[MIGRATION]
YES / NO


---

### 3️⃣ DSL Boundary Decision


[BOUNDARY]
xxx → FLAG / VAR / INVALID
理由：


---

### 4️⃣ Overall Decision


[REGISTRY ALIGNMENT]
PASS / FAIL

Tool unblock:
YES / NO


---

## 【目標】

完成後必須達成：


✔ registry coverage 完整
✔ 無 naming drift
✔ 無 DSL boundary ambiguity
✔ sync_registry_to_schema.py 可繼續執行


---

## ⚠️ 注意


這是 Governance 決策，不是實作任務。
不要修改 JSON，不要寫 code。
只做「規則與結論」。


---



---

# 🎯 補充（你可以理解但不用貼）

這份 prompt 做了三件關鍵事：


1. 把 tool BLOCK → 轉成 governance 決策問題
2. 把模糊 audit → 變成強制決策（YES/NO）
3. 確保結果可以直接 unblock production


---

如果你下一步要，我可以幫你：

👉 直接模擬 Governance 回答（幫你一次解完這批）
