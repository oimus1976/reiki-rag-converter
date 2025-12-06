import json
import os
import argparse
import html
from typing import List, Dict, Any


class IdGenerator:
    """l000000000 / e000000001 形式のIDを連番で払い出す簡易ジェネレータ"""

    def __init__(self) -> None:
        self.line_index = 0
        self.elem_index = 1

    def next_line_id(self) -> str:
        line_id = f"l{self.line_index:09d}"
        self.line_index += 1
        return line_id

    def next_elem_id(self) -> str:
        elem_id = f"e{self.elem_index:09d}"
        self.elem_index += 1
        return elem_id


def make_eline(inner_html: str, ids: IdGenerator) -> str:
    """DVD例規HTMLに近い .eline ラインを生成"""
    line_id = ids.next_line_id()
    return (
        f'<div>\n'
        f'<div id="{line_id}" class="eline">{inner_html}</div>\n'
        f'</div>\n'
    )


# ----------------------------------------------------------------------
# タイトル・公布日・番号
# ----------------------------------------------------------------------


def render_title_block(meta: Dict[str, Any], ids: IdGenerator) -> List[str]:
    title = meta.get("title", "")
    prom = meta.get("promulgation", {}) or {}
    date = prom.get("date") or ""
    number = prom.get("number") or ""

    elines: List[str] = []

    # 条例タイトル（p.title-irregular）
    e_title = ids.next_elem_id()
    inner = (
        '<div class="head">'
        f'<p class="title-irregular"><span id="{e_title}" class="cm">'
        f'{html.escape(title)}'
        '</span></p>'
        '</div>'
    )
    elines.append(make_eline(inner, ids))

    # 公布日（p.date）
    if date:
        e_date = ids.next_elem_id()
        inner = (
            '<div class="head">'
            f'<p class="date"><span id="{e_date}" class="cm">'
            f'{html.escape(date)}'
            '</span></p>'
            '</div>'
        )
        elines.append(make_eline(inner, ids))

    # 条例番号（p.number）
    if number:
        e_num = ids.next_elem_id()
        inner = (
            '<div class="head">'
            f'<p class="number"><span id="{e_num}" class="cm">'
            f'{html.escape(number)}'
            '</span></p>'
            '</div>'
        )
        elines.append(make_eline(inner, ids))

    return elines


# ----------------------------------------------------------------------
# 条・項・号
# ----------------------------------------------------------------------


def render_article_block(block: Dict[str, Any], ids: IdGenerator) -> List[str]:
    """
    article ブロック:
    {
      "type": "article",
      "num": 3,
      "title": {"text": "名称及び位置", ...},
      "clauses": [...]
    }
    """
    num = block.get("num")
    title_info = block.get("title") or {}
    title_text = title_info.get("text", "")
    clauses = block.get("clauses") or []

    elines: List[str] = []

    if num is None or not clauses:
        return elines

    # 1つ目の項は div.article 内に「(条タイトル)」「第X条」「本文」をまとめる
    first_clause = clauses[0]
    clause_text = first_clause.get("text", "")

    # 条タイトル（括弧書き）
    e_title = ids.next_elem_id()
    title_span = ""
    if title_text:
        title_span = (
            f'<p class="title"><span id="{e_title}" class="cm">'
            f'({html.escape(title_text)})'
            '</span></p>'
        )

    # 第X条
    e_p = ids.next_elem_id()
    num_span_id = ids.next_elem_id()
    article_num_span = (
        f'<span id="{num_span_id}" class="num cm">'
        f'第{num}条'
        '</span>　'
    )
    clause_span = (
        f'<span class="clause"><span id="{ids.next_elem_id()}" '
        f'class="p cm">{html.escape(clause_text)}</span></span>'
    )
    num_p = (
        f'<p id="{e_p}" class="num">'
        f'{article_num_span}'
        f'{clause_span}'
        '</p>'
    )

    inner = f'<div class="article">{title_span}{num_p}</div>'
    elines.append(make_eline(inner, ids))

    # 1つ目の項に紐づく号
    items = first_clause.get("items") or []
    elines.extend(render_items(items, ids))

    # 2項目以降は .eline > div.clause で出力
    for clause in clauses[1:]:
        elines.extend(render_clause_line(clause, ids))

    return elines


def render_clause_line(clause: Dict[str, Any], ids: IdGenerator) -> List[str]:
    """第2項以降の行を生成（div.clause）"""
    num = clause.get("num")
    text = clause.get("text", "")
    items = clause.get("items") or []

    elines: List[str] = []

    # 項本体
    e_p = ids.next_elem_id()
    num_span = ""
    if num is not None:
        num_span = (
            f'<span id="{ids.next_elem_id()}" class="num cm">'
            f'{num}'
            '</span>　'
        )

    p_html = (
        f'<p id="{e_p}" class="num">'
        f'{num_span}'
        f'<span id="{ids.next_elem_id()}" class="p cm">'
        f'{html.escape(text)}'
        '</span>'
        '</p>'
    )
    inner = f'<div class="clause">{p_html}</div>'
    elines.append(make_eline(inner, ids))

    # この項に紐づく号
    elines.extend(render_items(items, ids))

    return elines


def render_items(items: List[Dict[str, Any]], ids: IdGenerator) -> List[str]:
    """号（div.item）の生成"""
    elines: List[str] = []
    for item in items:
        num = item.get("num")
        text = item.get("text", "")
        e_p = ids.next_elem_id()
        num_span = ""
        if num is not None:
            num_span = (
                f'<span id="{ids.next_elem_id()}" class="num cm">'
                f'({num})'
                '</span>　'
            )
        p_html = (
            f'<p id="{e_p}" class="num">'
            f'{num_span}'
            f'<span id="{ids.next_elem_id()}" class="p cm">'
            f'{html.escape(text)}'
            '</span>'
            '</p>'
        )
        inner = f'<div class="item">{p_html}</div>'
        elines.append(make_eline(inner, ids))
    return elines


# ----------------------------------------------------------------------
# 表
# ----------------------------------------------------------------------


def render_table_block(block: Dict[str, Any], ids: IdGenerator) -> List[str]:
    """
    table ブロック:
    {
      "type": "table",
      "caption": { "text": "第3条関係", "article": 3, ... },
      "rows": [
        [ { "text": "...", "colspan": 1, "rowspan": 1 }, ... ],
        ...
      ]
    }
    """
    rows = block.get("rows") or []
    elines: List[str] = []

    table_rows_html: List[str] = []
    for row in rows:
        cells_html: List[str] = []
        for cell in row:
            text = html.escape(str(cell.get("text", "")))
            colspan = cell.get("colspan")
            rowspan = cell.get("rowspan")
            attrs = []
            if colspan and colspan != 1:
                attrs.append(f'colspan="{int(colspan)}"')
            if rowspan and rowspan != 1:
                attrs.append(f'rowspan="{int(rowspan)}"')
            attr_str = (" " + " ".join(attrs)) if attrs else ""
            cells_html.append(f"<td{attr_str}>{text}</td>")
        table_rows_html.append("<tr>" + "".join(cells_html) + "</tr>")

    table_inner = "<table>" + "".join(table_rows_html) + "</table>"
    inner = (
        '<div class="table_frame"><div class="table-wrapper">'
        f"{table_inner}"
        '</div></div>'
    )
    elines.append(make_eline(inner, ids))

    return elines


# ----------------------------------------------------------------------
# 附則
# ----------------------------------------------------------------------


def render_supplement_block(block: Dict[str, Any], ids: IdGenerator) -> List[str]:
    """
    supplement ブロック:
    {
      "type": "supplement",
      "meta": { "label": "附則", "date_raw": "...", "number_raw": "..." },
      "articles": [ { "num": 1, "clauses": [ { "num": 1, "text": "..." } ] } ]
    }
    """
    meta = block.get("meta") or {}
    label = meta.get("label") or "附則"
    date_raw = meta.get("date_raw")
    number_raw = meta.get("number_raw")

    elines: List[str] = []

    # 見出し (.s-head)
    e_head = ids.next_elem_id()
    spans: List[str] = []

    # 附則タイトル
    spans.append(
        f'<span id="{ids.next_elem_id()}" class="title cm">'
        f'{html.escape(label)}'
        '</span>'
    )
    if date_raw:
        spans.append(
            f'<span id="{ids.next_elem_id()}" class="date cm">'
            f'{html.escape(date_raw)}'
            '</span>'
        )
    if number_raw:
        spans.append(
            f'<span id="{ids.next_elem_id()}" class="number cm">'
            f'{html.escape(number_raw)}'
            '</span>'
        )

    p_html = f'<p id="{e_head}" class="s-head">' + "".join(spans) + "</p>"
    elines.append(make_eline(p_html, ids))

    # 本文（附則内条の各項）
    articles = block.get("articles") or []
    for art in articles:
        clauses = art.get("clauses") or []
        for clause in clauses:
            text = clause.get("text", "")
            e_p = ids.next_elem_id()
            p_body = (
                f'<p style="text-indent:1em;margin-left:0em;" '
                f'id="{e_p}" class="p">'
                f'<span id="{ids.next_elem_id()}" class="p cm">'
                f'{html.escape(text)}'
                '</span>'
                '</p>'
            )
            inner = f'<div class="clause">{p_body}</div>'
            elines.append(make_eline(inner, ids))

    return elines


# ----------------------------------------------------------------------
# ブロックディスパッチ
# ----------------------------------------------------------------------


def render_blocks(blocks: List[Dict[str, Any]], ids: IdGenerator) -> List[str]:
    elines: List[str] = []
    for block in blocks:
        btype = block.get("type")
        if btype == "article":
            elines.extend(render_article_block(block, ids))
        elif btype == "table":
            elines.extend(render_table_block(block, ids))
        elif btype == "supplement":
            elines.extend(render_supplement_block(block, ids))
        else:
            # 未対応タイプは素のテキストとして出力（保険）
            text = block.get("text")
            if text:
                e = ids.next_elem_id()
                inner = (
                    f'<p id="{e}" class="p">'
                    f'<span id="{ids.next_elem_id()}" class="p cm">'
                    f'{html.escape(str(text))}'
                    '</span></p>'
                )
                elines.append(make_eline(inner, ids))
    return elines


# ----------------------------------------------------------------------
# HTMLドキュメント全体
# ----------------------------------------------------------------------


def build_html_document(meta: Dict[str, Any]) -> str:
    ids = IdGenerator()
    title = meta.get("title", "")
    prom = meta.get("promulgation", {}) or {}
    date = prom.get("date") or ""
    number = prom.get("number") or ""
    blocks = meta.get("blocks") or []

    elines: List[str] = []
    elines.extend(render_title_block(meta, ids))
    elines.extend(render_blocks(blocks, ids))

    elines_html = "".join(elines)

    # secondary は最小限の情報のみ生成（heading + datenumber）
    secondary = (
        '<div id="secondary">\n'
        '<div class="heading-area">\n'
        f'<h2 class="heading-lv2A">{html.escape(title)}</h2>\n'
        '</div>\n'
        f'<p class="datenumber-area mt04">{html.escape(date)}　{html.escape(number)}</p>\n'
        '</div>\n'
    )

    html_doc = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="ROBOTS" content="NOARCHIVE">
<title>{html.escape(title)}</title>
<link rel="stylesheet" type="text/css" href="reiki.css">
</head>
<body>
<div id="wrapper">
<div id="container">
<!-- 本文 -->
<div id="primary" class="joubun showhistory">
<div id="primaryInner">
<div id="primaryInner2">
{elines_html}</div>
</div>
</div>
<!-- /本文 -->
{secondary}<!-- secondary --></div>
</div>
</body>
</html>
"""
    return html_doc


# ----------------------------------------------------------------------
# メタファイル読み込み / 生成
# ----------------------------------------------------------------------


def load_meta_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_from_meta(meta_path: str, output_dir: str) -> str:
    meta = load_meta_file(meta_path)
    html_text = build_html_document(meta)
    law_id = meta.get("id") or os.path.splitext(os.path.basename(meta_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{law_id}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    return out_path


# ----------------------------------------------------------------------
# CLI エントリポイント
# ----------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic Reiki HTML from meta JSON (v0.2)."
    )
    parser.add_argument(
    "--meta-dir",
    default="synthetic_html_meta/v0.2",
    help="Directory containing meta JSON files (v0.2 only).",
)
    parser.add_argument(
        "--output-dir",
        default="synthetic_html",
        help="Directory to write generated HTML files.",
    )

    args = parser.parse_args()

    meta_dir = args.meta_dir
    output_dir = args.output_dir

    if not os.path.isdir(meta_dir):
        print(f"meta dir not found: {meta_dir}")
        return

    generated: List[str] = []
    for fname in sorted(os.listdir(meta_dir)):
        if not fname.lower().endswith(".json"):
            continue
        path = os.path.join(meta_dir, fname)
        out_path = generate_from_meta(path, output_dir)
        generated.append(out_path)

    print("Generated synthetic HTML files:")
    for p in generated:
        print(" -", p)


if __name__ == "__main__":
    main()
