# tests/fixtures/reiki_html

Annex / CSV 表抽出系 pytest が参照する **実条例 HTML fixture** を置くディレクトリ。

## 方針（2026-11-04 決定）

- 以下の pytest は実条例 DOM を前提とするため、CI でも実行する。
- そのため、必要な HTML **3 件のみ** を本ディレクトリに Git 追跡対象として固定する。
- `reiki-html/` は引き続きローカル専用（`.gitignore` 対象）。テストからは参照しない。
- テストを skip / deselect して CI を通す運用は採らない。

## 必要ファイル

| ファイル | 内容（テスト上の役割） | 参照テスト |
|---|---|---|
| `k518RG00000219.html` | かつらぎ町使用料、手数料、督促及び延滞金条例。別表第1・第2（表あり） | test_detect_annex_candidate_regions / test_extract_csv_cells_from_real_annex2 / test_extract_tables_from_region / test_find_annex_headings / test_iter_annex_blocks / test_iter_annex_items_fee_ordinance_annex2 / test_render_annex_region_to_markdown |
| `k518RG00000205.html` | かつらぎ町税条例。明示的な別表見出しあり | test_detect_annex_candidate_regions |
| `k518RG00000030.html` | かつらぎ町地籍調査推進委員会規則。別表への参照のみ（別表本体なし） | test_find_annex_headings / test_iter_annex_blocks |

## 取得元

- かつらぎ町例規集（公開サイト）から 2026-11-04 に取得し、無加工で保存した
  - `https://www.town.katsuragi.wakayama.jp/reiki/reiki_honbun/<ファイル名>`
- 文字コード UTF-8、改行 CRLF（原本のまま）

## 取り扱い

- ファイルは原本（公開サイトまたはローカル `reiki-html/`）を **無加工で保存** する。
- 内容を変更する場合は、テスト期待値への影響を確認し CHANGELOG に記録する。
- fixture の追加は、テストが必要とする最小限に留める。
