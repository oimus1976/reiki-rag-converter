---
title: synthetic HTML 設計書
project: reiki-rag-converter
category: design
version: 0.1
status: draft
created: 2025-12-04
updated: 2025-12-04
---

# 1. 目的と位置づけ

## 1.1 目的

本設計書は、例規HTML変換プロジェクトにおいて利用する **synthetic HTML（合成例規HTML）** の仕様を定める。

synthetic HTML は、以下を主目的とする **テスト・検証用データ** であり、本番業務で変換対象とする実条例HTMLとは明確に区別される。

- validate_reiki_structure（構造解析）および例外チェックツール v3.1 の検証用データ
- convert_reiki（HTML→Markdown風TXT変換）の回帰テスト用データ
- GitHub 上で公開可能な「条例ライクなHTMLデータセット」
- 他自治体が自前の条例HTMLを公開せずにパーサ改善に参加できる土台

## 1.2 実HTMLとの関係

- **実HTML**
  - 例：かつらぎ町条例HTML（`#primaryInner2` 配下の `.eline` 構造）  
  - validate / convert は **直接実HTMLを入力として利用する**
  - 著作権上の理由から GitHub には公開しない

- **synthetic HTML**
  - DOM構造・class構造は実HTMLを模倣する
  - テキスト（条文内容・地名・日付等）は完全創作とし、実条例の文言を引用しない
  - GitHub に同梱し、pytest + CI で利用する

> 他市町村がツールを導入する際、HTMLを synthetic に変換してから利用する必要はない。  
> synthetic はあくまで **開発・検証のための教材セット** である。

---

# 2. スコープ

## 2.1 synthetic HTML が担う範囲

- DVD 等で提供される **実HTMLの構造パターンを抽象化** し、代表的な揺れを網羅した「模型条例」をHTMLとして生成する。
- 対象とする構造：
  - 見出し（タイトル・公布日・番号）
  - 条・項・号
  - 附則（複数・抄あり）
  - 表（table）※本則中・附則中
  - 別記様式リンク・サムネイル
  - リスト構造（ul/li）
- 以下は synthetic v0.1 のスコープ外（将来拡張）：
  - iframe 埋め込み
  - 章・節レベルの階層構造
  - iframe 内の別HTML

## 2.2 synthetic HTML が行わないこと

- 実条例のテキストを引用・改変しない
- RAG用Markdownを直接生成しない（変換は convert_reiki の責務）:contentReference[oaicite:5]{index=5}
- 本番運用時に実条例HTMLの代わりとして投入されることを前提としない

---

# 3. 用語

- **実HTML**：ベンダが提供する実際の条例HTMLファイル
- **synthetic HTML**：本設計に基づき生成される合成条例HTML
- **synthetic law**：1つの synthetic HTML に対応する1条例相当の単位
- **パターンセット**：特定の構造（例：表＋別記様式＋複数附則）を再現した synthetic law のグループ

---

# 4. synthetic HTML の構造要件

## 4.1 HTML全体の基本構造

実HTMLと同等の大枠構造を持つが、最低限に簡略化する。

- `<html lang="ja">`
- `<head>`  
  - `meta charset`, `title`, `link rel="stylesheet" href="reiki.css"` 程度
- `<body>`
  - `#wrapper > #container`
    - `#primary.joubun.showhistory`
      - `#primaryInner > #primaryInner2`
        - 本文 `.eline` 群
    - `#secondary`（見出し・条項目次など、必要最小限）

※ `script` や `ipad.js` 等は、必要であればダミーで残すが、パーサは `#primaryInner2` と `.eline` のみを利用する想定。

## 4.2 `.eline` ブロック

各 `.eline` は「1行分の論理構造」を表す。実HTMLと同様に、以下のパターンを synthetic で再現する。

- 見出し行（タイトル・日付・番号）
- 本則条文（`div.article`）
- 項・号行（`div.clause` / `div.item`）
- 附則見出し（`.s-head`）
- 表（`div.table_frame > div.table-wrapper > table`）
- 別記様式（`div.form_section` と `div.xref_frame`）

---

# 5. クラス・タグ設計

## 5.1 利用する class セット

基本的には KNOWN_CLASSES（例外チェック v3.1）で定義されたクラスのみを利用する。:contentReference[oaicite:7]{index=7}

- CORE: `eline`, `article`, `clause`, `item`, `num`, `title`, `title-irregular`, `date`, `number`, `p`, `s-head`
- TABLE: `table_frame`, `table-wrapper`, `b-on`, `bb-on`, `br-on`, `l-edge`, `r-edge`, `t-edge`, `b-edge`, `fixed-colspec`
- LINK: `inline`, `quote`, `xref_frame`
- 装飾・UI系: `cm`, `word-space`, `open`, `close`, `noicon`, `main_rules`, `supplement` など

## 5.2 禁止事項

- KNOWN_CLASSES に存在しない class を原則追加しない（未知classは例外検出対象となるため）:contentReference[oaicite:8]{index=8}  
- 実際の自治体名・住所・個人名など実在情報をそのまま使わない（ synthetic 用の架空名に置き換える）

---

# 6. パターン設計

synthetic v0.1 では、次の代表パターンを必須カバーとする。各パターンは 1 つ以上の synthetic law で表現する。

## 6.1 P1: シンプル本則＋単一附則

- タイトル・公布日・番号あり
- 条：1〜3条程度、条名付き／なし両方
- 項・号を持たないシンプル構造
- 附則1本（施行日条文のみ）

→ 「最もベーシックな構造」で、validate/convert の正常系を確認する。

## 6.2 P2: 項・号を持つ本則（用語定義型）

- 第2条に用語定義条（条名付き）
- `div.item` による `(1)`, `(2)` 形式の号を含む
- 条中に「次の各号」「当該各号」などのリンク（`inline quote`）を含む:contentReference[oaicite:9]{index=9}

→ 項・号の検出・整列ロジックの検証に用いる。

## 6.3 P3: 表（table_in_main）

- 本則第3条の本文の直後に表を持つ（`table_frame > table-wrapper > table` 構造）:contentReference[oaicite:10]{index=10}  
- `<thead>` と本文行 `<tr>` を含む
- 表は2〜3列程度、Markdown表変換の基本パターンとして利用

→ convert_reiki における Markdown表変換の黄金パターン。:contentReference[oaicite:11]{index=11}

## 6.4 P4: 複数附則（附則見出しの揺れ）

- 「附則」のみ
- 「附則（令和X年条例第Y号）」形式
- 「附則（令和X年条例第Y号）抄」のように末尾に注記が付く形式

→ validate の附則ブロック分割ロジック・重複メタ検出（S103）の検証に用いる。:contentReference[oaicite:12]{index=12}

## 6.5 P5: 別記様式付き

- 本則中の条で「別記様式」を参照するリンク（`div.form_section`）を持つ
- 別記様式のサムネイル画像（`div.xref_frame` 内 `img`）を持つ:contentReference[oaicite:13]{index=13}

→ convert側での「別記様式をどうテキスト化するか」の設計検証に使う。

## 6.6 P6: リスト構造（ul/li）

- `div.item` の中に `<ul><li>` を含む構造を最低1例用意
- validate 側の構造イベント `ul_in_item` 検出のテストに用いる:contentReference[oaicite:14]{index=14}

---

# 7. synthetic HTML 生成パラメータ

synthetic generator（別設計）のために、1 synthetic law を生成する際のパラメータ群をここで定義する。

## 7.1 メタ情報

- `law_id`: 例 `synRG00000001`（実IDと被らないプレフィックス `syn` を付与）
- `title`: 架空の条例名
- `promulgation_date`: 元号＋和暦
- `number`: 「条例第X号」「規程第Y号」など

## 7.2 構造フラグ

- `has_article_titles`: 条名（括弧書き）の有無
- `article_count`: 本則の条数
- `has_items`: 項・号を持つか
- `has_table_main`: 本則中の表の有無
- `has_table_supplement`: 附則中の表の有無（v0.1では任意）
- `supplement_count`: 附則の本数
- `has_supplement_note`: 「抄」等の注記の有無
- `has_form_section`: 別記様式の有無
- `has_ul_in_item`: ul/liリストの有無

## 7.3 テキスト生成ポリシー

- 文言は完全に創作する（例：架空自治体「サンプル町」、架空地区名など）
- 法律名・条番号も例示として創作する（既存法令名を丸ごと引用しない）
- 条名・項・号の構造は実例をなぞりつつ、具体的な名詞・表現は変える

---

# 8. ファイル構成と命名規則

## 8.1 ディレクトリ構成（案）

- `synthetic_html/`
  - `synRG00000001_basic.html`（P1）
  - `synRG00000002_items.html`（P2）
  - `synRG00000003_table_main.html`（P3）
  - `synRG00000004_multi_supplement.html`（P4）
  - `synRG00000005_form_section.html`（P5）
  - `synRG00000006_ul_in_item.html`（P6）
- 将来：
  - `synthetic_html_meta.json`（各ファイルのパターン種別等のメタ情報）

## 8.2 pytest / CI との連携

- `tests/synthetic/` に、対応する Golden TXT を配置：
  - `tests/synthetic/expected/synRG00000001.txt` 等
- E2Eテストでは：
  1. synthetic_html/*.html を validate & convert
  2. 生成TXTと `expected/*.txt` を diff
  3. 例外・構造イベントの発生件数も検証

---

# 9. 利用方法

## 9.1 開発者視点

1. synthetic_html を GitHub レポジトリに同梱
2. 開発時：
   - 実HTMLでバグが起きた場合、そのパターンを抽象化して synthetic パターンを1つ追加
   - pytest の Golden を更新
3. CI：
   - プルリク時に synthetic セット＋一部実HTML（ローカル専用）で E2E を実行

## 9.2 他自治体の開発者視点

- 自治体独自DOMに対応させたいが、実条例HTMLは公開できない場合：
  1. 自治体内でのみ使う「実例 → synthetic パターン定義」のマッピングを作る
  2. プロジェクトの synthetic パターンを拡張する PR を送り、パーサ側にそのDOM揺れを取り込む
  3. 手元の実条例で動作検証（この部分は各自治体ローカル）

---

# 10. 今後の拡張（v0.2 以降）

- colspan / rowspan を含む表の synthetic パターン追加
- 章・節構造（`第1章 総則` など）の追加
- 改正文モデル v0.6 に対応した synthetic（改正附則・読み替え条文）の追加
- RAG チャンク分割テスト用に「極端に長い条文」を持つ synthetic の追加

---

# 11. まとめ

- synthetic HTML は **開発・検証・OSS協調のための安全な“教材”** であり、本番変換対象ではない。
- DOM・class構造は実HTMLに忠実に、テキストは完全創作とすることで、著作権と技術要件の両方を満たす。
- 本設計 v0.1 では、最低限必要な6パターン（P1〜P6）を定義し、今後のバグや新たな揺れへの対応は synthetic パターンの追加で行う。
