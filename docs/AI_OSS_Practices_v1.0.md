# AI × OSS Development Practices（v1.0）
本書は、ChatGPT を OSS 開発プロジェクトに統合し、  
安定かつ継続的に開発メンバー（アーキテクト/エンジニア）として活用するための  
実践手法をまとめたものである。

本手法は reiki-rag-converter プロジェクトをモデルケースとして体系化した。

---

## 1. 基本理念：AI-as-Architect
ChatGPT を「指示を出す相手」としてではなく、  
**プロジェクトのアーキテクトとして扱うこと** を基本理念とする。

このためには以下の3要素が不可欠である：

1. **設計書（Design Docs）** を最優先情報源とする  
2. **PROJECT_STATUS.md を唯一の進行基準点（SSoT）とする**  
3. **PROJECT_GRAND_RULES.md に基づく行動規範を課す**

---

## 2. 文書体系（AI が参照すべきファイルの最小構成）
ChatGPT プロジェクト側には、以下の 4 種類だけを配置する。

### 2.1 設計書層（Design Layer）
- Design_convert  
- Design_validate  
- Design_synthetic_html  
- Design_synthetic_generator  
- test_plan  
- test_e2e_design  
- requirements

→ 設計意図・仕様・制約を ChatGPT が常に参照する。

### 2.2 実装層（Implementation Layer）
- convert_xxx.py  
- validate_xxx.py  
- synthetic_generator_xxx.py  

→ ChatGPT がコード生成や修正を行う際の唯一の根拠。

### 2.3 meta 層（Generation Definition）
- synthetic_html_meta/v0.2/*.json  
- synthetic_html_meta_template.json  

→ Synthetic HTML の生成とテストの基盤。

### 2.4 CI 層（Verification Layer）
- .github/workflows/e2e.yml  

→ Golden diff・smoke test・依存環境などを定義。

### 2.5 置いてはならないもの
- output_md  
- synthetic_html  
- logs  
- __pycache__  
- 古いバージョンのコード  
- 実条例 HTML（著作権のため）

AI の判断空間が汚染されるため厳禁とする。

---

## 3. PROJECT_STATUS.md（Single Source of Truth）
プロジェクトの進行状態はすべて **PROJECT_STATUS.md** で管理する。

### 3.1 Next Action の原則
- Next Action は常に 1つ  
- ChatGPT はタスクを勝手に切り替えない  
- 新しい提案は「候補」として提示し、採用するかは人間が決める

### 3.2 作業完了後のルール
- 完了タスクは Completed へ移動  
- 必ず Next Action を空にせず保持する  
- 進捗の整合性保全は ChatGPT の義務とする

---

## 4. Grand Rules（ChatGPT 行動規範）
AI が OSS の長期開発に参加するための最低条件。

### 4.1 設計整合性最優先
- 設計書と矛盾する提案は禁止  
- 実装変更前に影響範囲（設計・CI・テスト）を必ず検証する

### 4.2 安易な修正禁止
- CI が通るだけの理由で設計項目を削除してはならない  
- 例：converted_at を出力から消す等

### 4.3 CI を壊さない
- smoke test  
- Golden diff  
- 非決定項目の除外  
- exit code 5 の防止  

は絶対原則。

### 4.4 ファイル削減原則
- ChatGPT プロジェクト内のファイルは 25 個以内  
- 不必要な生成物は排除する

### 4.5 PENTA による多角検討
必要に応じて Brain One〜Five により  
仕様検討・設計レビューを行う。

---

## 5. CI / Golden Diff / 再現性
OSS の品質確保の要となる。

### 5.1 Golden diff 原則
- Golden は「正解データ」であり、安易に上書きしない  
- 差分は構造変化が本当にあった場合のみ見直す  

### 5.2 非決定項目は diff 対象外
例：  
`converted_at:`

→ CI の揺れを防ぎ、テストの安定性を担保。

### 5.3 Synthetic → Validate → Convert の完全再現性
meta から同じ HTML が生成され、  
変換結果が常に Golden と一致する必要がある。

---

## 6. ChatGPT 開始テンプレート（起動プロトコル）
セッション開始時は次を貼る：

```

このプロジェクトでは以下を厳守してください。

* PROJECT_GRAND_RULES.md を遵守する
* PROJECT_STATUS.md の Next Action のみ実行対象
* 設計書と実装に基づいて判断する
* CI と Golden diff の安定性を最優先する
* 必要に応じて PENTA で多角的検討を行う

```

これにより「プロジェクトモード」に入り、  
ChatGPT は OSS 開発メンバーとして安定行動する。

---

## 7. プロジェクト成熟度モデル（AI x OSS）
OSS プロジェクトに AI を統合する場合、次の5段階を踏む。

1. 文書整備  
2. CI 安定化  
3. SSoT（PROJECT_STATUS.md）確立  
4. ガバナンス整備（Grand Rules）  
5. 機能拡張フェーズ（AI-assisted 開発）

あなたのプロジェクトはすでに「4」まで完了し、  
次は「5：本格的な機能進化段階」にある。

---

## 8. 結論：AI は適切に枠組みを与えれば OSS 開発を支えるアーキテクトとなる
本手法は、  
「AI を OSS の長期開発に安全に統合する方法」として  
普遍的に再利用可能な実践モデルとなる。

