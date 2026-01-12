---
title: Reproducibility_Break_and_Recovery_2026-01
project: reiki-rag-converter
scope: execution-input-contract / dev-environment
date: 2026-01-09
status: resolved
related_issues:
  - "#9 Coverage Policy逸脱"
  - "#10 Clause誤認識"
---

# Merge 不整合による再現性崩壊と復旧記録

## 1. 概要（何が起きたか）

Clause 正規化（Q4）および附則抽出（Q8）の修正を main に反映した後、  
**別端末でリポジトリを pull しても同一の結果が得られない**事象が発生した。

具体的には：

- main ブランチ上で pytest が **大量に失敗**
- 同一コミットを参照しているはずなのに、
  - 端末 A：pytest 通過
  - 端末 B：pytest 失敗
- 原因が **コード差分では説明できない状態**だった

これは実装バグではなく、  
**Git マージ状態と依存解決手順の不整合**に起因する問題だった。

---

## 2. 事象の詳細（一次情報）

### 2.1 Git の状態

一時点で以下の状態が確認された：

- `fix/normalize-clause-structure` に最新実装が存在
- `main` ブランチがその内容を **まだ取り込んでいない端末が存在**
- `git branch -vv` / `git log --decorate` により、
  - ローカル main
  - origin/main
  - fix ブランチ
  が **一致していないことが判明**

結果として：

> 「同じ main を使っているつもりでも、  
> 実際には異なる履歴を参照している端末が存在する」

という状態だった。

---

### 2.2 pytest 失敗内容

別端末での pytest 失敗は以下に集約された：

```bash
ModuleNotFoundError: No module named 'chardet'
```

失敗箇所：

- `convert_reiki_v2.7.py`
- `validate_reiki_structure_v0.5.2.py`
- synthetic E2E tests（全滅）

---

## 3. 原因分析（なぜ起きたか）

### 原因①：Git マージの事実不一致

- 修正は **実際には fix ブランチに存在**
- main には **push されていない端末が存在**
- 端末ごとに「見ている main」が異なっていた

→ **再現性以前に、履歴が一致していなかった**

---

### 原因②：依存関係の宣言不足

- `chardet` は以下で使用されていた：
  - `convert_reiki_v2.7.py`
  - `validate_reiki_structure_v0.5.2.py`

- しかし：
  - pyproject.toml に依存として明示されていなかった
  - requirements.txt には記載されていたが、
    - **pyproject.toml を正とする現行のパッケージ構成では参照されない**

結果：

> 端末 A（過去に chardet を手動 install）
> 端末 B（クリーン環境）

で挙動が分岐。

---

### 原因③：トップレベルパッケージ名の衝突

- reiki-rag-converter と gov-llm-e2e-testkit の双方に
  `customized_question_set` という同名パッケージが存在
- editable install / PYTHONPATH / CI 実行順により、
  import 解決先が環境ごとに変動
- 結果として：
  - ローカルでは通るが CI で落ちる
  - 端末 A と B で import される実体が異なる
  という「再現性崩壊」を引き起こした

本問題は Coverage Policy や生成ロジック以前の、
**名前空間設計上の構造問題**である。

#### 対策：トップレベルパッケージ名の衝突（恒久対策）

> customized_question_set を
> reiki_rag_customized_question_set に rename し、
> 名前空間レベルでの衝突可能性を除去した。
>
> これにより：
>
> - editable install
> - 複数リポジトリ共存
> - CI / ローカル / 新端末
>
> の import 解決が完全に安定した。

---

## 4. 実施した対応（何をやったか）

### 4.1 Git の正規化

- fix ブランチの内容を main に **明示的に push**
- 全端末で以下を実施：

```bash
git pull origin main
git log --oneline --decorate
```

→ **全端末で main の履歴が一致**

---

### 4.2 依存関係の正規化

#### 実施した対応

- chardet を明示的に pip install
- pytest 全通過を確認

#### 恒久対応（今後の正）

```toml
[project]
dependencies = [
  "beautifulsoup4>=4.12",
  "chardet>=5.2.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0"
]
```

#### 正式なセットアップ手順を確立

```bash
pip install -e .[dev]
python -m pytest -q
```

→ 新規端末でも pytest が **即座に再現成功**

---

## 5. 結果（現在の状態）

- Clause 正規化（Q4）：✅ 正常
- 附則抽出（Q8）：✅ 正常
- Golden Ordinance 10本 手動確認：✅ 全件生成
- pytest：
  - 31 passed
  - 3 skipped
- **別端末再現性：確立**

---

## 6. 教訓（再発防止）

### 教訓①

> 「自分の端末で動く」は、
> **再現性の証明ではない**  
> 特に「過去に手動で入れた依存」がある端末は、
> 再現性検証に使ってはいけない

### 教訓②

> Git の merge 状態が曖昧なままでは、
> pytest の結果は信頼できない

### 教訓③

> requirements.txt があっても、
> **pyproject.toml が正でなければ意味がない**

---

### 教訓④

> Python におけるトップレベルパッケージ名は、
> 設計上の契約であり、実装詳細ではない  
> 「名前が被る」こと自体が、再現性リスクである

---

## 7. 恒久ルール（今後の運用）

- 依存関係は **pyproject.toml を唯一の正**
- requirements.txt は補助（明示コメント必須）
- 新端末検証は必ず：

```bash
pip install -e .[dev]
python -m pytest -q
```

- main に入っていない修正は「存在しないもの」と扱う

---

## 8. ステータス

- 本件は **設計・運用ともに解決済み**
- Issue #9 / #10 の後続影響は解消
- Execution Input Contract の再現性は回復
