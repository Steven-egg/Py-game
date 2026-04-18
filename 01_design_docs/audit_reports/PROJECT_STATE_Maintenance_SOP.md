# 01_design_docs/audit_reports/PROJECT_STATE_Maintenance_SOP.md

## 1. 目的
本文件定義在 **Evolution Mode: CLOSED** 狀態下，手動維護 `PROJECT_STATE.json` 的標準作業程序，確保「治理軌跡」的完整性，防止 AI 記憶丟失或設計漂移。

## 2. 審核檢查清單 (Manual Audit Check-list)
在手動更新 `PROJECT_STATE.json` 中的 `last_validation_date` 前，必須逐項確認以下 5 個關鍵點：

1.  **[ ] DSL 名稱規範化**：確認所有 `03_data` 中的指令皆符合 `02_specs` 的 Canonical 命名（例如：已將 `flag.int_add` 修正為 `flag.add_int`）。
2.  **[ ] 權限邊界檢查**：確認 `03_data` 中無任何 `var.*` 指令（此類指令僅限引擎層使用）。
3.  **[ ] 註釋同步更新**：確認 `notes` 欄位已記錄本次審計發現的重大變更（如：Deprecated 警告或新導入的規格）。
4.  **[ ] 結構完整性**：確認本次更新未變動 `PROJECT_STRUCTURE.md` 定義的頂層目錄結構。
5.  **[ ] 備份確認**：確認對話中的審計報告（如 `DSL-4_Consistency_Matrix.md`）已同步至 Git 備份區域。

## 3. 同步節奏與觸發條件
嚴禁隨意修改狀態文件。僅在以下情境下允許執行手動同步：

* **審計任務完成**：完成如 DSL-4 的數據比對審核，並產出對應 Markdown 報告後。
* **版本里程碑達成**：當 `02_specs` 完成小版本更迭（如 1.3.0 -> 1.3.1）且數據層已對齊時。
* **治理決策（DD）執行後**：當新的設計決策被批准並反映在文件層級後。

---

## 4. 治理執行指令 (DSL-6 Action)
請將上述內容保存至路徑：`01_design_docs/audit_reports/PROJECT_STATE_Maintenance_SOP.md`。
*(註：根據隔離原則，路徑鎖定於 audit_reports/ 以利追蹤)*

---

## ⚠️ Spec Auditor 關鍵提醒 (Governance Protocol)

1.  **備份同步**：請務必將此 **PROJECT_STATE_Maintenance_SOP.md** 內容同步至您的 Git 備份區域（如 `audit_reports/`），這對於維持長期的 AI 協作脈絡至關重要。
2.  **建立治理軌跡**：每一次手動修改 `PROJECT_STATE.json` 後，建議在 Git 提交訊息中引用此 SOP 的檢查點編號。
3.  **嚴禁實作**：再次提醒，DSL-6 僅規範「程序」，目前禁止產生任何用於修改 JSON 的 Python 代碼。