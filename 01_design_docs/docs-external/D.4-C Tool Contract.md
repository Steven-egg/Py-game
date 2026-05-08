# 治理清債已完成（REG-003 + INDEX + TASK_CONTRACT）

---

# 📄 D.4-C Tool Contract

## `sync_registry_to_schema.py`

---

## 1. Purpose（目的）

將既有 `03_data` JSON 檔案：

* 與 **Registry（SSOT）對齊**
* 與 **Schema（02_specs）建立明確關聯**
* 並在過程中執行 **DSL Governance（DD-020）違規攔截**

---

## 2. Scope（範圍）

### ✔ In Scope

* `03_data/quests`
* `03_data/items`
* `03_data/monsters`
* （未來可擴充至 registries）

---

### ❌ Out of Scope

* 不修改 schema 定義（02_specs）
* 不修改 DSL 規範
* 不生成 registry
* 不處理 engine runtime

---

## 3. Inputs（輸入）

### 3.1 Data Files

* `03_data/**/*.json`

### 3.2 Registry Files（SSOT）

* `03_data/registries/*.json`

### 3.3 Schema Mapping


SCHEMA_MAP = {
  "quests": "02_specs/schema/quest.schema.json",
  "items": "02_specs/schema/item.schema.json",
  "monsters": "02_specs/schema/monster.schema.json",
}


---

## 4. Core Responsibilities（核心職責）

---

### 4.1 Schema URI Injection（延續原工具能力）

條件：


若 JSON 不含 "$schema" → 補上
若已存在 → 不覆寫


---

### 4.2 Registry Validation（新增）

對每個 JSON：


- 必須存在唯一 ID
- ID 必須存在於對應 registry


否則：


→ FAIL（中止）


---

### 4.3 DSL Governance Enforcement（DD-020）

掃描 JSON 中的 effect / condition：

---

#### ❌ Non-canonical DSL（禁止）


flag.int_add


---

#### ❌ Engine-only DSL（禁止）


var.add


---

### 行為：


若偵測 → 中止整個流程（hard fail）


---

## 5. Processing Flow（處理流程）


Load registry
   ↓
Scan JSON files
   ↓
Validate ID in registry
   ↓
Scan DSL usage
   ↓
If ANY violation → abort
   ↓
Inject $schema
   ↓
Write file


---

## 6. Output（輸出）

### 成功：


[OK] file patched
[SKIP] already has $schema


---

### 失敗：


[ERROR] registry mismatch
[ERROR] DSL violation: flag.int_add
[ERROR] DSL violation: var.add


---

## 7. Failure Policy（失敗策略）

### 🔴 Hard Fail（強制中止）

以下任一成立：

* registry 不存在 ID
* DSL 違規
* JSON 無法解析

👉 必須：


立即停止，不允許 partial success


---

## 8. Constraints（約束）

### Governance Constraints

* ❌ 不允許修改 registry
* ❌ 不允許修改 schema
* ❌ 不允許自動修正 DSL

---

### Production Constraints

* 僅允許：

  * 讀取
  * 驗證
  * 補 `$schema`

---

## 9. Extension（未來擴充）

未來可加入：

* registry auto-link（schema ↔ registry）
* schema version validation
* content coverage report

---

## 10. Relationship to Existing Tool

| 工具                           | 狀態               |
| ---------------------------- | ---------------- |
| `add_schema_uri.py`          | Prototype        |
| `sync_registry_to_schema.py` | Formal Tool（本契約） |

---

# 🎯 給你怎麼用（很重要）

你在新對話中：

👉 不要貼程式
👉 貼這份 Contract

然後說：


請依此 Contract 實作 sync_registry_to_schema.py


---

# 🧠 最關鍵一句話

👉 你現在做的轉變是：

> 從「寫工具」
> → 變成
> **「定義工具行為，再讓 Production 實作」**

---

# 如果你下一步要做

我可以幫你：

* 🔧 對照你現有 `add_schema_uri.py` → **列出最小改動 patch**
* 🧪 或直接幫你設計 **驗證測試（MVL for tool）**

你現在已經正式進入 D.4-C 了。
