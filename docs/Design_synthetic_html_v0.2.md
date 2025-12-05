---
title: synthetic HTML 設計書
project: reiki-rag-converter
category: design
version: 0.2
status: active
created: 2025-12-04
updated: 2025-12-05
---

# 1. 改訂概要（v0.1 → v0.2）

本設計書は、例規HTML変換プロジェクトにおける **synthetic HTML（合成例規HTML）** の仕様を定める。

v0.1 では、基本的な位置づけと P1〜P6 のパターン定義を行った。  
v0.2 では PENTA レビュー結果を踏まえ、以下の点を拡張・明確化した。

- **新規パターン P7〜P10 を追加**
  - P7：章・節構造
  - P8：別記様式（PDFリンク形式）
  - P9：長大条文（チャンク分割テスト用）
  - P10：意図的エラー synthetic（validate の error/warn テスト用）
- **DOM 揺れ仕様（余計な div ネスト、s-head 揺れ、table-wrapper 欠落など）を定義**
- **synthetic HTML 自動生成エンジン（synthetic generator v0.1）の I/F を定義**
- **synthetic_html_meta.json のスキーマを定義**
- **CI/E2E を synthetic ベースで運用できるようにするための前提情報を整理**

synthetic HTML は、実条例 HTML を公開せずに OSS としてパーサ開発を継続するための「安全な教材セット」である。

---

# 2. synthetic HTML の位置づけ

## 2.1 実HTMLとの関係

- **実HTML**
  - 例：ベンダーが提供する条例HTML（`#primaryInner2` 配下に `.eline` を持つ構造）
  - validate / convert は、実務上は実HTMLを直接入力として利用する
  - 著作権の可能性があるため GitHub には公開しない

- **synthetic HTML**
  - DOM・class 構造は実HTMLを模倣する
  - 条文テキスト・地名・日付等の内容は完全創作とし、実在条例からの引用は行わない
  - GitHub に同梱し、pytest + CI のテストデータセットとして利用する
  - DOM 揺れやエラーケースを自由に仕込むことで、パーサの堅牢性を検証する

## 2.2 synthetic HTML の用途

- validate / convert / 例外検査ツールの挙動確認・回帰テスト
- CI（GitHub Actions）での E2E テスト（実HTML非依存）
- 他自治体が実HTMLを公開せずにパーサ改善に参加できる仕組みの土台
- DOM 揺れパターンのカタログ化

本番運用（他自治体での条例変換）では、合成HTMLに変換してから使用する必要はない。  
synthetic はあくまで **開発・検証・共同開発のための教材** である。

---

# 3. スコープ

## 3.1 synthetic HTML がカバーする構造

synthetic HTML は、以下の構造要素をカバーする。

- 条例タイトル・公布日・番号
- 条・項・号
- 章・節（v0.2 で追加）
- 附則（複数本・抄あり）
- 表（本則中・附則中）
- 別記様式（画像リンク・PDFリンク）
- リスト構造（ul/li）
- 意図的なエラー（構造欠落・未知classなど）

## 3.2 スコープ外（将来拡張）

- iframe 埋め込みコンテンツの中身
- 複数ファイルにまたがる条例（本則と別冊）への対応
- 極端に特殊なベンダー固有classの全網羅

---

# 4. 基本HTML構造

## 4.1 HTML全体

synthetic HTML の基本的な外形は、ぎょうせい系HTMLを参考にした最小構成とする。

```html
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <title>サンプル町○○条例</title>
    <link rel="stylesheet" href="reiki.css">
  </head>
  <body>
    <div id="wrapper">
      <div id="container">
        <div id="primary" class="joubun showhistory">
          <div id="primaryInner">
            <div id="primaryInner2">
              <!-- ここに .eline 群が入る -->
            </div>
          </div>
        </div>
        <div id="secondary">
          <!-- 必要に応じて見出しや概要を置く -->
        </div>
      </div>
    </div>
  </body>
</html>
````

パーサは `#primaryInner2` 配下の `.eline` のみを主対象とし、
`script` 等の付帯要素は synthetic では原則省略する。

## 4.2 `.eline` 単位

`.eline` は「画面上の1行相当の論理ユニット」として扱う。

* 見出し行（タイトル・公布日・番号）
* 条・項・号の本文行
* 附則見出し・附則本文行
* 表・別記様式・リストを含む行

synthetic では、実HTML同様に `.eline` 配下にさらに `div` が入れ子になる揺れも再現する（4.3 参照）。

---

# 5. クラス・タグ方針

## 5.1 利用する主な class

原則として「実HTMLで既知のクラス群」のみを使用し、未知classは P10（エラー synthetic）専用とする。

* CORE:

  * `eline`, `article`, `clause`, `item`, `num`, `title`, `title-irregular`, `date`, `number`, `s-head`
* TABLE:

  * `table_frame`, `table-wrapper`, `b-on`, `bb-on`, `br-on`,
    `l-edge`, `r-edge`, `t-edge`, `b-edge`, `fixed-colspec`
* LINK/参照:

  * `inline`, `quote`, `xref_frame`, `form_section`
* その他（必要に応じて）:

  * `chapter`, `section`（章・節表現用）

## 5.2 禁止事項

* 実在する自治体名・住所・人名・条例名などをそのまま使用しない
* KNOWN_CLASSES にないクラスを標準的パターンに追加しない（未知classは例外検出対象とする）
* 実条例テキストをコピー＆ペーストしない（必ず文章を創作する）

---

# 6. パターン設計（P1〜P10）

synthetic v0.2 では、少なくとも以下の 10 パターンを公式セットとして用意する。

## P1：基本構造（最小）

* タイトル／公布日／番号あり
* 条：1〜3 条（条名あり・なし両方）
* 項・号なし
* 附則1本（施行日だけを規定）

目的：validate/convert の正常系の確認。

---

## P2：用語定義型（項・号）

* 第2条が用語定義条
* `div.item` による `(1)(2)…` の号を持つ
* 文中に「次の各号に掲げる…」などを含む
* inline quote を挿入して DOM 揺れも再現

目的：項・号検出・整列ロジックの検証。

---

## P3：表（table_in_main）

* 本則第○条の本文直後に表を持つ
* 構造例：

  ```html
  <div class="eline">
    <div class="table_frame">
      <div class="table-wrapper">
        <table class="b-on">
          <thead>…</thead>
          <tbody>…</tbody>
        </table>
      </div>
    </div>
  </div>
  ```
* 表見出し（caption相当）もMarkdown表に反映する

目的：convert による Markdown表変換の挙動検証。

---

## P4：複数附則（抄付き）

* 附則が 2〜3 本存在
* 「附則」「附則（令和X年条例第Y号）」など複数形式
* 「附則（令和X年条例第Y号）抄」のような注記付きも含む

目的：validate の附則ブロック分割・S103（附則メタ重複）検出テスト。

---

## P5：別記様式（画像）

* 本則の一条に「別記様式第1号」のような記述
* 別記様式を表す `div.form_section` とサムネイル画像を持つ：

  ```html
  <div class="form_section">
    <p>別記様式第1号</p>
    <div class="xref_frame">
      <img src="form001.png" alt="別記様式第1号">
    </div>
  </div>
  ```

目的：別記様式の取扱い方針・convert結果の妥当性確認。

---

## P6：リスト構造（ul/li）

* 号の本文に `<ul><li>` を含む：

  ```html
  <div class="item">
    <p class="num">(1)</p>
    <div class="body">
      <p>次の各号に掲げる事項</p>
      <ul>
        <li>一　サンプル項目A</li>
        <li>二　サンプル項目B</li>
      </ul>
    </div>
  </div>
  ```

目的：DOM混在（p + ul/li）の耐性検証。

---

## P7：章・節構造

* 「第1章 総則」「第2章 雑則」等を持つ
* 必要に応じて「第1節 基本」を含む

例：

```html
<div class="eline">
  <p class="chapter">第1章 総則</p>
</div>
<div class="eline">
  <p class="section">第1節 通則</p>
</div>
```

目的：章・節を見出しレベルとして扱う convert 拡張の準備。

---

## P8：別記様式（PDFリンク）

* 別記様式が PDF として提供されるパターン：

  ```html
  <div class="xref_frame">
    <a href="form001.pdf" class="form-link">別記様式第1号（PDF）</a>
  </div>
  ```

目的：PDF形式の様式参照をどのようにテキスト化するか検証。

---

## P9：長大条文（チャンク分割用）

* 3,000〜8,000 文字クラスの長文条を含む
* 項・号・段落を跨ぐ構造
* inline quote も複数含む

目的：RAG 用チャンク分割・長文処理の挙動検証。

---

## P10：意図的エラー synthetic

validate の error/warn を検証するため、以下のケースを混在させる。

* `#primaryInner2` が欠落 → `NO_PRIMARY_INNER`
* `.eline` が存在しない → `NO_ELINE`
* タイトルや番号が欠落
* 附則メタはあるが本文が空 → S101_SUPP_WITHOUT_BODY 相当
* 附則メタが重複 → S103_SUPP_DUPLICATE_META 相当
* 未知class（例：`class="unknown-x"`）を混入

目的：異常系ハンドリングと severity 判定のテスト。

---

# 7. DOM揺れ仕様

synthetic では、現実の揺れを再現するため、以下の揺れパターンを注入可能とする。

## 7.1 余計な div ネスト

```html
<div class="eline">
  <div>
    <div class="article">
      ...
    </div>
  </div>
</div>
```

* ネストの段数は 0〜2 程度の範囲で変化させる。

## 7.2 s-head（附則見出し）の揺れ

代表的なスタイル：

* A: `p.s-head > span.title / span.date / span.number`
* B: `div.s-head > span.title ...`（p ではなく div）
* C: `span.s-head` にタイトル文字列を直書き（子要素なし）

パラメータ例：`s_head_style = "A" | "B" | "C"`

## 7.3 table-wrapper 欠落

標準：

```html
<div class="table_frame">
  <div class="table-wrapper">
    <table>…</table>
  </div>
</div>
```

揺れ：

```html
<div class="table_frame">
  <table>…</table>
</div>
```

→ convert が余計な div に依存せず動作することを確認する。

## 7.4 inline quote の階層揺れ

```html
<p>
  <span>
    <a class="inline quote">次号</a>
  </span>
</p>
```

階層は 1〜3 段階程度で可変。

## 7.5 属性揺れ

* `style="text-indent:1em"` の有無
* `style="margin-left:0em"` の有無

属性依存のロジックに陥らないよう、揺れを意図的に混在させる。

---

# 8. synthetic generator v0.1 インターフェース

synthetic HTML 自動生成器の I/F を以下のように定義する。

```yaml
generate_synthetic_html(
  pattern_id: str,       # "P1"〜"P10"
  law_id: str,           # "synRG00000001" など
  seed: int,             # DOM揺れの乱数シード
  flags:
    has_nested_div: bool
    s_head_style: str          # "A" | "B" | "C"
    table_wrapper_style: str   # "normal" | "missing"
    inline_quote_depth: int    # 0〜3
    has_ul_in_item: bool
    supplement_count: int
  meta:
    title: str
    promulgation_date: str     # "令和X年Y月Z日"
    number: str                # "条例第X号"など
    notes: str | null
) -> {
  html_text: str,
  meta_json: object
}
```

生成結果は以下のように保存する。

* `synthetic_html/{law_id}.html`
* `synthetic_html_meta/{law_id}.json`

---

# 9. synthetic_html_meta.json のスキーマ

各 synthetic law（1 HTML）ごとにメタ情報を JSON として持つ。

```json
{
  "law_id": "synRG00000001",
  "pattern": "P3",
  "title": "サンプル町駐車場条例",
  "structure": {
    "article_count": 5,
    "has_items": true,
    "has_table_main": true,
    "supplement_count": 2
  },
  "dom_variation": {
    "nested_div": true,
    "s_head_style": "B",
    "inline_depth": 2,
    "table_wrapper": "missing"
  },
  "anomalies": [],
  "created_at": "2025-12-05"
}
```

P10 のようなエラー synthetic の場合は `anomalies` にエラーコードを格納する。

---

# 10. ディレクトリ構成（v0.2）

```text
synthetic_html/
  synRG00000001_P1_basic.html
  synRG00000002_P2_items.html
  synRG00000003_P3_table.html
  synRG00000004_P4_multi_supplement.html
  synRG00000005_P5_form_image.html
  synRG00000006_P6_ul_list.html
  synRG00000007_P7_chapter.html
  synRG00000008_P8_form_pdf.html
  synRG00000009_P9_long_article.html
  synRG00000010_P10_error_cases.html

synthetic_html_meta/
  synRG00000001.json
  synRG00000002.json
  ...
```

---

# 11. テスト／CI との連携

* CI（GitHub Actions）では synthetic_html を対象に E2E テストを実施する。

* 各パターンについて：

  1. validate を実行 → 構造エラー／イベントを JSON 出力
  2. convert を実行 → Markdown/TXT 出力
  3. Golden TXT と比較（完全一致）
  4. validate 結果と convert 結果の整合性をチェック

* 実条例HTMLを入力とする E2E は、著作権上の理由から CI では実施せず、ローカル専用とする。

---

# 12. 今後の拡張（v0.3 以降）

* colspan/rowspan を含む表の synthetic パターン（P11〜）の追加
* 改正文（読み替え・施行期日）を含む synthetic の追加
* 行政文書（規程・要綱等）用の synthetic
* RAG チャンク分割ロジック検証用の超長文 synthetic セット

synthetic HTML は、これらの拡張のたびにパターン・meta・generator を追加していくことで、
例規パーサの品質と OSS としての拡張性を両立させる。

---

````

---

## 🧾 次の Git 操作メモ

1. 上記を `docs/Design_synthetic_html_v0.2.md` として保存  
2. そのあと以下を実行：

```bash
cd C:/Users/user/reiki-rag-converter

git add docs/Design_synthetic_html_v0.2.md
git add CHANGELOG.md  # v0.2 追加を一行追記しておくのがおすすめ

git commit -m "Add Design_synthetic_html_v0.2 with extended patterns P1–P10 and generator/meta spec"
git push origin main
````

CHANGELOG 追記例：

```markdown
## [Unreleased]
- Add Design_synthetic_html_v0.2 (P1–P10, DOM variation, generator & meta spec)
```

---

