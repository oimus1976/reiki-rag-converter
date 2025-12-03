import os
import re
import argparse
import datetime
import chardet
from bs4 import BeautifulSoup

# ============================================================
# convert_reiki_v2.7 (本文抽出修正版)
# - 例規HTML (#primaryInner2 配下の .eline) を解析し
#   RAG 向けの Markdown 風 TXT に変換する。
# - v2.6 をベースにした GitHub 移行版（互換仕様）。
# ============================================================

DEFAULT_SOURCE_DIR = "reiki_honbun"
DEFAULT_OUTPUT_DIR = "output_md"
CONVERTER_VERSION = "2.7"


ZEN_TO_HAN = str.maketrans("０１２３４５６７８９", "0123456789")


def normalize_digits(s: str) -> str:
    return s.translate(ZEN_TO_HAN)


def read_html_with_encoding(path: str) -> str:
    """chardet でエンコーディング判定しつつ HTML を読み込む。"""
    with open(path, "rb") as f:
        raw = f.read()
    enc = chardet.detect(raw)["encoding"] or "utf-8"
    try:
        return raw.decode(enc, errors="ignore")
    except Exception:
        return raw.decode("utf-8", errors="ignore")


def extract_title_meta(soup: BeautifulSoup):
    """条例タイトル・公布日・番号を抽出。"""
    main = soup.select_one("#primaryInner2")
    title = None
    date_raw = None
    number_raw = None

    if main:
        t = main.select_one("p.title-irregular")
        if t:
            title = t.get_text(strip=True)

        d = main.select_one("p.date")
        if d:
            date_raw = d.get_text(strip=True)

        n = main.select_one("p.number")
        if n:
            number_raw = n.get_text(strip=True)

    if title is None:
        h2 = soup.select_one("#secondary h2")
        if h2:
            title = h2.get_text(strip=True)

    return title, date_raw, number_raw


def normalize_japanese_date(date_raw: str):
    """(平成10年3月30日) → 1998-03-30"""
    if not date_raw:
        return ""

    ERA_BASE = {
        "明治": 1867,
        "大正": 1911,
        "昭和": 1925,
        "平成": 1988,
        "令和": 2018,
    }

    s = re.sub(r"[()（）\s]", "", date_raw)
    s = s.replace("施行", "")
    s = normalize_digits(s)
    m = re.search(r"(明治|大正|昭和|平成|令和)(\d+)年(\d+)月(\d+)日", s)
    if not m:
        return date_raw

    era, y, mo, d = m.groups()
    base = ERA_BASE.get(era)
    if not base:
        return date_raw

    year = base + int(y)
    try:
        dt = datetime.date(year, int(mo), int(d))
    except ValueError:
        return date_raw

    return dt.isoformat()


def extract_law_id_from_filename(filename: str) -> str:
    """k518RG00000080.html → k518RG00000080"""
    base = os.path.basename(filename)
    if base.lower().endswith(".html"):
        return base[:-5]
    return os.path.splitext(base)[0]


def detect_article_info(eline) -> tuple:
    """
    .eline 内の div.article を探し、
    条番号と条名（括弧書きタイトル）を返す。
    """
    article = eline.find("div", class_="article")
    if not article:
        return None, None

    num_span = article.select_one("p.num > span.num.cm")
    title_span = article.select_one("p.title span.cm")

    article_num = None
    article_title = None

    if num_span:
        txt = num_span.get_text(strip=True)
        m = re.fullmatch(r"第([0-9０-９]+)条", txt)
        if m:
            article_num = normalize_digits(m.group(1))

    if title_span:
        article_title = title_span.get_text(strip=True)

    return article_num, article_title


def is_s_head(eline) -> bool:
    """附則見出しか？"""
    if "s-head" in eline.get("class", []):
        return True
    if eline.find(class_="s-head"):
        return True
    return False


def extract_supplement_heading(eline) -> str:
    """附則見出しの Markdown 文字列を作る。"""
    s = eline.find(class_="s-head") or eline
    title_span = s.find("span", class_="title")
    date_span = s.find("span", class_="date")
    num_span = s.find("span", class_="number")

    label = title_span.get_text(strip=True) if title_span else "附則"

    tail_parts = []
    if date_span:
        tail_parts.append(date_span.get_text(strip=True))
    if num_span:
        tail_parts.append(num_span.get_text(strip=True))

    if tail_parts:
        return f"{label}（{' '.join(tail_parts)}）"
    return label


def extract_plain_text_from_eline(eline) -> str:
    """本文テキストの抽出。"""
    text = eline.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text


def html_table_to_markdown(table, caption: str | None = None) -> str:
    """<table> → Markdown表 変換。"""
    rows = []

    thead = table.find("thead")
    if thead:
        for tr in thead.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if cells:
                rows.append(cells)

    body_trs = table.find_all("tr")
    for tr in body_trs:
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)

    if not rows:
        return ""

    header = rows[0]
    data_rows = rows[1:] if len(rows) > 1 else []
    cols = len(header)

    def to_row(cells):
        padded = list(cells) + [""] * (cols - len(cells))
        return "| " + " | ".join(padded[:cols]) + " |"

    md_lines = []

    if caption:
        md_lines.append(f"### 【表：{caption}】")
        md_lines.append("")

    md_lines.append(to_row(header))
    md_lines.append("| " + " | ".join(["---"] * cols) + " |")

    for r in data_rows:
        md_lines.append(to_row(r))

    md_lines.append("")
    return "\n".join(md_lines)


def convert_single_html(path: str, output_dir: str):
    """単一 HTML ファイルを Markdown 風 TXT に変換する。"""
    html = read_html_with_encoding(path)
    soup = BeautifulSoup(html, "html.parser")

    main = soup.select_one("#primaryInner2")
    if not main:
        print(f"[WARN] #primaryInner2 が見つかりません: {path}")
        return

    elines = main.select(".eline")
    if not elines:
        print(f"[WARN] .eline が見つかりません: {path}")
        return

    law_id = extract_law_id_from_filename(path)
    title, date_raw, number_raw = extract_title_meta(soup)
    date_normalized = normalize_japanese_date(date_raw) if date_raw else ""
    converted_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # frontmatter
    frontmatter_lines = [
        "---",
        f"id: {law_id}",
        f"title: {title or ''}",
        f"number: {number_raw or ''}",
        f"promulgation_date: {date_raw or ''}",
        f"promulgation_date_normalized: {date_normalized}",
        f"source_html: {os.path.basename(path)}",
        f"converted_at: {converted_at}",
        f"converter_version: {CONVERTER_VERSION}",
        "tags:",
        "  - 例規",
        "  - 条例",
        "---",
        "",
    ]

    body_lines: list[str] = []

    # タイトル
    if title:
        body_lines.append(f"# {title}")
        body_lines.append("")

    for el in elines:

        # 附則見出し
        if is_s_head(el):
            heading = extract_supplement_heading(el)
            body_lines.append(f"## {heading}")
            body_lines.append("")
            continue

        # 表
        table_frame = el.find("div", class_="table_frame")
        table = table_frame.find("table") if table_frame else el.find("table")
        if table:
            caption = None
            article_num, _ = detect_article_info(el)
            if article_num:
                caption = f"第{article_num}条関係"
            md_table = html_table_to_markdown(table, caption=caption)
            if md_table:
                body_lines.append(md_table)
            continue

        # 条見出し
        article_num, article_title = detect_article_info(el)
        if article_num:
            if article_title:
                body_lines.append(f"## 第{article_num}条（{article_title}）")
            else:
                body_lines.append(f"## 第{article_num}条")
            body_lines.append("")

            # ★★★【重要】条の本文抽出（追加修正）★★★
            clause_span = el.select_one("div.article p.num span.clause")
            if clause_span:
                clause_text = clause_span.get_text(" ", strip=True)
                clause_text = re.sub(r"\s+", " ", clause_text)
                if clause_text:
                    body_lines.append(clause_text)
                    body_lines.append("")

            continue

        # 通常本文
        text = extract_plain_text_from_eline(el)
        if not text:
            continue

        # 簡易号判定
        if re.match(r"^[（(][0-9０-９]+[)）]", text):
            clean = re.sub(r"^[（(]\s*([0-9０-９]+)\s*[)）]\s*", r"(\1) ", text)
            body_lines.append(f"- {clean}")
        else:
            body_lines.append(text)

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{law_id}.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(frontmatter_lines + body_lines))

    print(f"[OK] {path} -> {out_path}")


def convert_directory(source_dir: str, output_dir: str):
    """ディレクトリ内の *.html を一括変換"""
    if not os.path.isdir(source_dir):
        print(f"[ERROR] ソースディレクトリが存在しません: {source_dir}")
        return

    files = [f for f in os.listdir(source_dir) if f.lower().endswith(".html")]
    files.sort()

    if not files:
        print(f"[WARN] HTML ファイルが見つかりません: {source_dir}")
        return

    for fname in files:
        in_path = os.path.join(source_dir, fname)
        try:
            convert_single_html(in_path, output_dir)
        except Exception as e:
            print(f"[ERROR] 変換中に例外が発生しました: {in_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Reiki HTML into AI/RAG-ready Markdown-like TXT files."
    )
    parser.add_argument(
        "--source",
        "-s",
        default=DEFAULT_SOURCE_DIR,
        help=f"入力HTMLディレクトリ（デフォルト: {DEFAULT_SOURCE_DIR}）",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"出力先ディレクトリ（デフォルト: {DEFAULT_OUTPUT_DIR}）",
    )

    args = parser.parse_args()

    convert_directory(args.source, args.output)


if __name__ == "__main__":
    main()
