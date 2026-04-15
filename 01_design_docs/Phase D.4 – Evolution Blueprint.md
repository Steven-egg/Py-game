以下為 **Phase D.4 – Evolution 啟動藍圖**（設計級，無實作），已與 **DD-020（Effect DSL Governance Charter）**對齊，並遵守 **Lock + Controlled Evolution**。此藍圖明確任務拆解、順序依賴、門檻（gates）與風險控管。

---

# Phase D.4 – Evolution Blueprint

**前提**

* 版本錨點：Spec **1.3.0** / Engine **1.0.0**
* 治理：先通過 **DD-020 正式化 → Evolution Mode: OPEN** 後方可執行
* SSOT：`save.game_state`（flags / inventory / vars / current_location）

---

## 一、總體目標（D.4 Objectives）

1. **Naming Alignment（Engine ↔ Schema）**
   將 engine 對齊 `flag.add_int`（消除 `flag.int_add` 漂移）

2. **Contract Formalization（var.add 升格評估）**
   在不破壞「專用指令優先」前提下，決定是否升格為 Content DSL

3. **Registry–Schema 自動對齊（SSOT 自動化）**
   建立 Registry 驅動的 Schema 注入機制

4. **Effect Coverage 完整化**
   補齊 Behavior Coverage，擴展至 `quest.*`、並規劃高語境 DSL（battle/ui/scene）

---

## 二、階段切分（Phased Execution）

### **D.4-A：Preparation（治理開啟）**

* **A1. DD-020 正式化（必須）**
* **A2. 切換 Evolution Mode → OPEN**
* **A3. 定義成功標準（DoD）**

  * 無 Naming Drift
  * 無 Boundary Violation
  * Coverage Matrix ≥ 目標門檻

> **Gate A（進入實作前門檻）**：DD-020 已正式寫入、團隊同意 Scope 與風險

---

### **D.4-B：Naming Alignment（優先）**

**目標**：消除 `flag.int_add` vs `flag.add_int`

**任務**

* B1. Engine dispatcher 支援 canonical `flag.add_int`
* B2. 建立（暫時性）alias：`flag.int_add` → `flag.add_int`（向後相容）
* B3. 移除內部/文件中 non-canonical 使用（逐步）

**Gate B**

* 所有測試/fixtures 僅使用 `flag.add_int`
* alias 僅存在於 engine 內部（不可外溢至 content）

**風險**

* 破壞舊 fixture / 測試
* 解法：保留 alias 過渡 + regression

---

### **D.4-C：Registry–Schema Sync（核心基建）**

**目標**：建立 **Registry → Schema** 自動化關聯（SSOT 對齊）

**任務**

* C1. 定義 Sync Protocol（來源、輸出、衝突策略）
* C2. 設計 `sync_registry_to_schema` 工具（設計稿）
* C3. Schema 注入策略：

  * vars → enum / 約束
  * flags → pattern（如 `^flg\..+$`）
* C4. 將 Sync 納入驗證流程（pre-validation / CI）

**Gate C**

* Registry 成為變數唯一來源（新增變數需先註冊）
* Schema 不再手動維護重複列表（避免漂移）

**風險**

* Schema 膨脹或過度耦合
* 解法：vars 用 enum（小集合）、flags 用 pattern（大集合）

---

### **D.4-D：`var.add` Contract Decision（邊界升格或維持）**

**目標**：最終決定 `var.add` 的 DSL 地位

**候選策略**

1. **Maintain Engine-only（預設保守）**
2. **Controlled DSL（限制 target 必須在 registry）**
3. **Full DSL（完全開放）**

**任務**

* D1. 定義 contract（target / params / validation）
* D2. 與 registry 綁定（必要條件）
* D3. 與專用 DSL（如 `gold.add`）的優先規則

**Gate D（關鍵）**

* 不得破壞「專用指令優先」
* 必須與 registry 完整對齊
* 通過 Schema + Behavior Coverage

**風險**

* DSL 語意模糊化
* 解法：限制使用範圍或保留 engine-only

---

### **D.4-E：Effect Coverage Expansion（驗證擴張）**

**目標**：完成 Coverage Matrix

**優先順序**

* E1. **Tier 1（必須）**：`flag.*`、`stat.modify`
* E2. **Tier 2**：`quest.*`
* E3. **Tier 3（遞延/設計）**：`battle.*`、`ui.*`、`scene.*`、`loot.*`

**任務**

* 建立每個 effect 的：

  * Schema 測試
  * Behavior 測試
  * Negative 測試
* 更新 Coverage Matrix（可視化/文件化）

**Gate E**

* Tier 1 必須 Fully Covered 才可進入 D.4 結束評估
* 未覆蓋項目仍維持 Gate 阻斷（不得標 Ready）

---

### **D.4-F：Closure（收斂與回鎖）**

**任務**

* F1. 關閉 Evolution Mode → CLOSED
* F2. 更新版本（Spec 1.4.0（若有 schema 變更））
* F3. Regression 全綠（MVL + 新增 coverage）
* F4. 更新治理文件（DD-020 → finalized + 新 DD）

**Gate F（結束門檻）**

* 無 Naming Drift
* 無 Boundary Violation
* Coverage Matrix 達標
* 無跨層污染（Structure/Contract 乾淨）

---

## 三、順序依賴（Dependency Graph）

```text
A（治理開啟）
 ↓
B（Naming Alignment）
 ↓
C（Registry–Schema Sync）
 ↓
D（var.add 決策）
 ↓
E（Coverage Expansion）
 ↓
F（Closure）
```

**關鍵依賴說明**

* B → C：先統一 naming，避免同步工具注入錯誤名稱
* C → D：`var.add` 升格需依賴 registry–schema 對齊
* D → E：effect 定義穩定後，才能做完整 coverage
* E → F：coverage 完成才可關閉 evolution

---

## 四、風險總覽（Risk Map）

| 風險           | 類型         | 控制策略              |
| ------------ | ---------- | ----------------- |
| Naming 破壞舊內容 | Regression | alias 過渡 + 測試     |
| Schema 過度複雜  | 結構風險       | enum + pattern 分層 |
| var.add 語意污染 | DSL 風險     | 專用指令優先 + 限制升格     |
| Coverage 不完整 | 品質風險       | Gate 阻斷 + 分級驗證    |
| Registry 漂移  | SSOT 風險    | 強制註冊流程            |

---

## 五、成功指標（Success Criteria）

* ✅ Content 僅使用 canonical DSL（無 drift）
* ✅ 無 engine-only 指令滲入 content
* ✅ Schema / Engine / Registry 三層對齊
* ✅ Coverage Matrix 清晰且可驗證
* ✅ DSL 可預測、可擴展、可治理

---

## 六、最終結論

D.4 的本質不是「補功能」，而是：

> **將 Effect DSL 從「鬆散能力集合」進化為「Registry 驅動、Schema 約束、Coverage 驗證」的完整語言系統**

並完成：

* Naming → 對齊
* Boundary → 決策
* Coverage → 完整
* Registry → SSOT

---

如果你要進一步推進，我可以直接幫你做下一步：

👉 **D.4 任務拆解成實際 backlog（JIRA / 任務清單級）**
👉 或 **sync_registry_to_schema Protocol Spec（第一版正式規格）**
