以下清單僅屬 **Phase D.4 / Layer 5 / E1 Coverage Matrix 的設計級驗證規格**，不涉及任何 `02_specs` 或 `03_data` 修改；並以目前已確認的治理狀態為前提：**Evolution Mode: CLOSED**、合法且已驗證的 DSL 僅限 `gold.add`、`flag.set`、`flag.add_int`、`inventory.add`、`inventory.remove`，同時 `flag.int_add` 屬 non-canonical、`var.add` 屬 engine-only，皆不得進入 content。 

## E1 – Behavior Coverage 驗證清單

| 任務編號   | DSL      | 類別       | 驗證目標                          | 驗證輸入 / 前置條件                                   | 預期結果                                 | Gate / 備註                                      |
| ------ | -------- | -------- | ----------------------------- | --------------------------------------------- | ------------------------------------ | ---------------------------------------------- |
| E1-001 | gold.add | Schema   | 驗證 effect 名稱為合法 canonical DSL | effect 名稱=`gold.add`                          | 通過 schema gate                       | 僅合法 DSL 可進入 coverage matrix。                   |
| E1-002 | gold.add | Schema   | 驗證必填欄位齊備                      | effect 物件含 `type` 與數值參數                       | 通過 schema gate                       | 以「effect 必須具備可執行識別與必要參數」為檢核重點；屬設計清單，不改 schema。 |
| E1-003 | gold.add | Schema   | 驗證數值參數型別                      | 數值參數為整數，如 `10`                                | 通過 schema gate                       | 以可加總的 numeric / integer 為檢核重點。                 |
| E1-004 | gold.add | Behavior | 驗證 effect 執行後 state 寫入成功      | 初始 `save.game_state` 已載入；執行一次 `gold.add(+10)` | 金幣值增加 10，且狀態由 `save.game_state` 讀寫一致 | 狀態 SSOT 為 `save.game_state`。                   |
| E1-005 | gold.add | Behavior | 驗證可持久化                        | 執行 `gold.add(+10)` 後執行 save / reload          | reload 後金幣值仍維持增加後結果                  | 依既有 save / reload / persistence 驗證路徑設計。        |
| E1-006 | gold.add | Behavior | 驗證可重複累加                       | 連續執行兩次 `gold.add(+10)`                        | 金幣淨增加 20，無覆寫或重設                      | 檢查 dispatcher 的加法語意。                           |
| E1-007 | gold.add | Negative | 缺少數值參數                        | effect 僅有 `type=gold.add`，無數值參數               | schema / validation 失敗，阻止執行          | 未覆蓋或不合法 payload 不可放行。                          |
| E1-008 | gold.add | Negative | 參數型別錯誤                        | 數值參數傳入 `"10"`、`null`、`[]`                     | schema / validation 失敗，回報型別錯誤        | 預期為明確 reject，不得 silent cast。                   |
| E1-009 | gold.add | Negative | 非法 DSL 名稱漂移攔截                 | 將 effect 名稱改為 `gold.plus`                     | validation 失敗，阻止執行                   | 非 schema-defined DSL 一律 block。                 |

| 任務編號   | DSL      | 類別       | 驗證目標                 | 驗證輸入 / 前置條件                                     | 預期結果                                    | Gate / 備註                                |
| ------ | -------- | -------- | -------------------- | ----------------------------------------------- | --------------------------------------- | ---------------------------------------- |
| E1-010 | flag.set | Schema   | 驗證 effect 名稱合法       | effect 名稱=`flag.set`                            | 通過 schema gate                          | `flag.set` 為已驗證合法 DSL。                   |
| E1-011 | flag.set | Schema   | 驗證必填欄位齊備             | effect 含 `type`、flag 識別、布林值                     | 通過 schema gate                          | 核心欄位應能唯一描述「設定哪個 flag 為何值」。               |
| E1-012 | flag.set | Schema   | 驗證 flag 識別型別         | flag 名稱為字串                                      | 通過 schema gate                          | 不處理 registry 擴張，僅做現行 coverage 設計。        |
| E1-013 | flag.set | Schema   | 驗證設定值型別              | 設定值為 boolean                                    | 通過 schema gate                          | `true/false` 為主要檢核。                      |
| E1-014 | flag.set | Behavior | 驗證初次寫入               | 初始 `save.game_state.flags` 無該 key；執行 `flag.set` | `save.game_state.flags[target]` 被建立且值正確 | 狀態寫入位置必須是 SSOT。                          |
| E1-015 | flag.set | Behavior | 驗證覆寫更新               | 先將同一 flag 設為 `false`，再執行設為 `true`               | 最終值為 `true`                             | 驗證 set 語意為覆寫而非附加。                        |
| E1-016 | flag.set | Behavior | 驗證持久化                | 執行 `flag.set` 後 save / reload                   | reload 後 flag 值不變                       | 依既有 save persistence 檢核。                 |
| E1-017 | flag.set | Behavior | 驗證 condition 可讀取更新結果 | 執行後以 `flag.is_true` / `flag.is_false` 條件檢查      | 條件判斷與新值一致                               | condition support 已存在。                   |
| E1-018 | flag.set | Negative | 缺少 flag 識別           | 無 target flag 名稱                                | schema / validation 失敗                  | 必填欄位缺失應被攔截。                              |
| E1-019 | flag.set | Negative | 設定值非 boolean         | 值為 `"true"`、`1`、`null`                          | schema / validation 失敗                  | 預期明確型別報錯。                                |
| E1-020 | flag.set | Negative | 使用 non-canonical DSL | 將 effect 名稱寫成 `flag.int_add`                    | validation 失敗，阻止進 content / 執行          | `flag.int_add` 屬 forbidden naming drift。 |

| 任務編號   | DSL          | 類別       | 驗證目標                       | 驗證輸入 / 前置條件                    | 預期結果                                              | Gate / 備註                                           |
| ------ | ------------ | -------- | -------------------------- | ------------------------------ | ------------------------------------------------- | --------------------------------------------------- |
| E1-021 | flag.add_int | Schema   | 驗證 effect 名稱為 canonical    | effect 名稱=`flag.add_int`       | 通過 schema gate                                    | `flag.add_int` 是唯一合法命名；`flag.int_add` 禁止進 content。  |
| E1-022 | flag.add_int | Schema   | 驗證必填欄位齊備                   | effect 含 `type`、flag 識別、整數增量   | 通過 schema gate                                    | 設計重點為 target 與 delta。                               |
| E1-023 | flag.add_int | Schema   | 驗證增量型別                     | 增量為整數，可正可負                     | 通過 schema gate                                    | 僅檢查合法 numeric increment，不擴張 contract。               |
| E1-024 | flag.add_int | Behavior | 驗證既有整數 flag 累加             | 初始 `flags[target]=3`；執行 `+2`   | 結果為 `5`                                           | 驗證加法語意。                                             |
| E1-025 | flag.add_int | Behavior | 驗證初始缺值的處理                  | 初始 `flags[target]` 不存在；執行 `+2` | 應依 engine 現行 contract 決定：若允許初始化則結果為 `2`；若不允許則明確報錯 | 這筆需在 JIRA 標註「待以現行 engine 行為回填實測結果」，避免臆造。            |
| E1-026 | flag.add_int | Behavior | 驗證負增量                      | 初始值 `5`；執行 `-2`                | 結果為 `3`，且 state 正確持久化                             | 驗證減值仍屬 add_int 語意。                                  |
| E1-027 | flag.add_int | Behavior | 驗證持久化                      | 執行後 save / reload              | reload 後整數 flag 維持新值                              | 依 save.game_state persistence 路徑驗證。                 |
| E1-028 | flag.add_int | Behavior | 驗證與 `flag.int_compare` 的整合 | 執行增量後使用 `flag.int_compare` 檢查  | 比較結果與更新後數值一致                                      | `flag.int_compare` 為既有條件能力。                         |
| E1-029 | flag.add_int | Negative | 使用非 canonical 名稱           | effect 名稱=`flag.int_add`       | validation 失敗，阻止進 content / 執行                    | 明確測 naming drift block。                             |
| E1-030 | flag.add_int | Negative | 增量非整數                      | 值為 `"2"`、`true`、`null`         | schema / validation 失敗                            | 不接受隱式轉型。                                            |
| E1-031 | flag.add_int | Negative | target 非字串                 | target 傳入 `123`、`[]`           | schema / validation 失敗                            | 應有明確欄位型別錯誤。                                         |

| 任務編號   | DSL           | 類別       | 驗證目標           | 驗證輸入 / 前置條件                          | 預期結果                            | Gate / 備註                                            |
| ------ | ------------- | -------- | -------------- | ------------------------------------ | ------------------------------- | ---------------------------------------------------- |
| E1-032 | inventory.add | Schema   | 驗證 effect 名稱合法 | effect 名稱=`inventory.add`            | 通過 schema gate                  | `inventory.add` 為已驗證合法 DSL。                          |
| E1-033 | inventory.add | Schema   | 驗證必填欄位齊備       | effect 含 `type`、item 識別，必要時含數量       | 通過 schema gate                  | 檢核 item target 與數量欄位。                                |
| E1-034 | inventory.add | Schema   | 驗證 item 識別型別   | item id 為字串                          | 通過 schema gate                  | 不在此階段擴張 registry 規格。                                 |
| E1-035 | inventory.add | Schema   | 驗證數量型別         | quantity 為正整數；若省略則應符合現行 contract 預設值 | 通過 schema gate 或依現行 contract 報錯 | 這筆也建議在 JIRA 標註「依現行 engine contract 實測確認 default 行為」。 |
| E1-036 | inventory.add | Behavior | 驗證新增新物品        | 初始 inventory 無該 item；執行 add          | inventory 出現該 item，數量正確         | `inventory.has` 可用於後續讀取驗證。                           |
| E1-037 | inventory.add | Behavior | 驗證累加既有物品       | 初始已有數量 `2`；執行 add `+3`               | 結果數量為 `5`                       | 驗證加總非覆寫。                                             |
| E1-038 | inventory.add | Behavior | 驗證持久化          | 執行後 save / reload                    | reload 後 inventory 數量不變         | 依既有 save persistence。                                |
| E1-039 | inventory.add | Behavior | 驗證條件整合         | 執行 add 後使用 `inventory.has`           | 條件結果為 true                      | 反證 effect 與 condition 一致。                            |
| E1-040 | inventory.add | Negative | 缺少 item 識別     | 無 item id                            | schema / validation 失敗          | 必填缺失不得執行。                                            |
| E1-041 | inventory.add | Negative | 數量非法           | quantity=0、負數、字串                     | schema / validation 失敗          | 預期 reject 非正整數。                                      |
| E1-042 | inventory.add | Negative | 非法 DSL 名稱      | `inventory.plus`                     | validation 失敗                   | 非 schema-defined DSL 一律 block。                       |

| 任務編號   | DSL              | 類別       | 驗證目標           | 驗證輸入 / 前置條件                    | 預期結果                                | Gate / 備註                         |
| ------ | ---------------- | -------- | -------------- | ------------------------------ | ----------------------------------- | --------------------------------- |
| E1-043 | inventory.remove | Schema   | 驗證 effect 名稱合法 | effect 名稱=`inventory.remove`   | 通過 schema gate                      | `inventory.remove` 為已驗證合法 DSL。    |
| E1-044 | inventory.remove | Schema   | 驗證必填欄位齊備       | effect 含 `type`、item 識別，必要時含數量 | 通過 schema gate                      | 檢核 item target 與扣減量。              |
| E1-045 | inventory.remove | Schema   | 驗證數量型別         | quantity 為正整數；若省略則依現行 contract | 通過 schema gate 或依現行 contract 報錯     | 同樣標註需以現行 engine 行為回填。             |
| E1-046 | inventory.remove | Behavior | 驗證部分扣減         | 初始數量 `5`；執行 remove `2`         | 結果為 `3`                             | 驗證減法語意。                           |
| E1-047 | inventory.remove | Behavior | 驗證扣到 0 的處理     | 初始數量 `2`；執行 remove `2`         | 結果應為 `0` 或移除 key；需依現行 engine 行為實測回填 | 這筆需在 JIRA 標註為「實測決議型案例」。           |
| E1-048 | inventory.remove | Behavior | 驗證持久化          | 執行 remove 後 save / reload      | reload 後 inventory 維持扣減結果           | 依 save.game_state persistence 路徑。 |
| E1-049 | inventory.remove | Behavior | 驗證條件整合         | remove 後再跑 `inventory.has`     | 若數量足夠被扣光，條件應反映 false；若仍有庫存則反映 true  | 驗證 effect 與 condition 一致。         |
| E1-050 | inventory.remove | Negative | 移除不存在物品        | inventory 無該 item 即執行 remove   | 預期明確報錯或阻止負庫存；不得 silent underflow    | 此為 behavior-negative 關鍵案例。        |
| E1-051 | inventory.remove | Negative | 移除數量超過現有數量     | 初始數量 `1`；執行 remove `2`         | 預期明確報錯或阻止 underflow                 | 必須避免狀態進入非法負值。                     |
| E1-052 | inventory.remove | Negative | 數量非法           | quantity=0、負數、字串、null          | schema / validation 失敗              | 預期 reject 非正整數。                   |
| E1-053 | inventory.remove | Negative | 非法 DSL 名稱      | `inventory.delete`             | validation 失敗                       | 非 schema-defined DSL 一律 block。    |

## 共用 Gate 規則

| 任務編號   | 範圍               | 類別            | 驗證目標                                        | 驗證輸入 / 前置條件                                                                                | 預期結果                             | Gate / 備註                                      |
| ------ | ---------------- | ------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------- | ---------------------------------------------- |
| E1-054 | All verified DSL | Governance    | 驗證僅 5 個合法 DSL 被納入 coverage                  | Coverage Matrix 僅列 `gold.add / flag.set / flag.add_int / inventory.add / inventory.remove` | 通過                               | 這 5 個為目前 verified DSL。                         |
| E1-055 | All verified DSL | Governance    | 驗證 non-canonical DSL 被攔截                    | 任一案例將 `flag.add_int` 改寫為 `flag.int_add`                                                    | validation 失敗，BLOCK              | `flag.int_add` 為 naming drift。                 |
| E1-056 | All verified DSL | Governance    | 驗證 engine-only DSL 被攔截                      | 任一案例嘗試改用 `var.add`                                                                         | validation 失敗，BLOCK              | `var.add` 為 engine-only，不可進 content。           |
| E1-057 | All verified DSL | Governance    | 驗證未覆蓋 DSL 不可標 Ready                         | 對 coverage matrix 外的 effect 嘗試標記 Ready                                                     | Gate 拒絕                          | DD-020 明定未通過 Schema + Behavior Coverage 不可放行。  |
| E1-058 | All verified DSL | Persistence   | 驗證所有 behavior 測試均以 `save.game_state` 為最終比對面 | 執行 effect 後以 save / reload 驗證                                                              | state 變更與 reload 結果一致            | SSOT 已明確為 `save.game_state`。                   |
| E1-059 | All verified DSL | Scope Control | 驗證本清單不涉及 schema / content 修改                | 審查本清單內容                                                                                    | 僅為測試設計，不產生 02_specs / 03_data 變更 | 符合 Evolution Mode: CLOSED 的規劃限制。               |

## 補充說明

上表中有 4 類案例被我刻意標成「**需以現行 engine 行為回填實測結果**」：`flag.add_int` 對缺值 target 的初始化行為、`inventory.add`/`inventory.remove` 的省略 quantity 預設行為、以及 `inventory.remove` 扣到 0 後是保留 key 還是移除 key。原因是目前 SSOT 已明確規定治理邊界、合法 DSL 與 coverage 原則，但你提供的節錄文件沒有把這幾個執行細節寫成可直接宣稱的 contract；在 Evolution Mode: CLOSED 下，我只能把它們列成**必測項**，不能臆造為既定規格。這樣同步到 JIRA 會更乾淨，也更符合 DD-020 的治理精神。 

下一步最合理的是把這份表直接再整理成 **JIRA 匯入格式欄位版**。
