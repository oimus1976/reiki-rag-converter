# ============================================================
# validate_reiki_structure v0.5.3
#
# 主な更新点（v0.5.2 → v0.5.3）
# - JSON 出力時に set を安全にシリアライズ（list＋ソート）
# - CI（pytest）で synthetic_html ディレクトリを安定検証
# - 仕様は v0.5 系（条・項・号・附則解析）を継続
# ============================================================

import os
import sys
import json
import argparse
from bs4 import BeautifulSoup


# ============================================================
# JSON シリアライズ対応
# ============================================================

def _to_serializable(obj):
    """
    JSON に直接書けない型（set, tuple など）を安全に変換する。
    - set → sorted list
    - dict → 再帰処理
    - list/tuple → 再帰処理
    """
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}

    if isinstance(obj, set):
        return sorted(_to_serializable(v) for v in obj)

    if isinstance(obj, (list, tuple)):
        return [_to_serializable(v) for v in obj]

    return obj


def write_json(path: str, data):
    """出力前に JSON 互換型に変換してから保存する"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    serializable = _to_serializable(data)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)


# ============================================================
#  HTML パーサのユーティリティ
# ============================================================

def load_html(path: str):
    """HTML を BeautifulSoup に読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def extract_law_id(path: str):
    """ファイル名から条例IDを抽出"""
    return os.path.basename(path).replace(".html", "")


# ============================================================
# 条・項・号・附則の構造解析（v0.5 系仕様）
# ============================================================

def validate_html_structure(html_path: str):
    """
    synthetic / real HTML を解析し、構造メタ情報を返す。
    ここでは「例外（exception）」「イベント（event）」「クラス集合（classes）」などを返す。
    """
    soup = load_html(html_path)

    # 結果格納
    exceptions = []
    events = []
    classes = set()   # ★ v0.5.3 修正対象（JSON 前にリスト化する）

    # === タイトル抽出 ======================================================
    title_node = soup.find(id="title") or soup.find("h1") or soup.title
    title = title_node.get_text(strip=True) if title_node else ""

    # === 本文抽出（.eline → div.article → 条）===============================
    eline = soup.select_one(".eline")
    if not eline:
        exceptions.append({"type": "E001", "message": ".eline が見つからない"})
        return {
            "title": title,
            "exceptions": exceptions,
            "events": events,
            "classes": classes,
        }

    articles = eline.select("div.article")
    if not articles:
        exceptions.append({"type": "E002", "message": "div.article（条）が見つからない"})

    # 条ごとに解析
    for idx, art in enumerate(articles, 1):
        classes.update(art.get("class", []))

        # 項（div.clause）
        clauses = art.select("div.clause")
        for c in clauses:
            classes.update(c.get("class", []))

        # 号（div.item）
        items = art.select("div.item")
        for it in items:
            classes.update(it.get("class", []))

    # === 附則（.s-head 起点） ===============================================
    s_heads = soup.select(".s-head")
    if s_heads:
        events.append({"event": "found_supplement", "count": len(s_heads)})

    return {
        "title": title,
        "exceptions": exceptions,
        "events": events,
        "classes": classes,     # ★ JSON 書き込み時に list 化される
    }


# ============================================================
# メイン：ディレクトリ単位で validate 実行
# ============================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="HTML ファイルを含むディレクトリ")
    parser.add_argument("--output", help="出力フォルダ（未指定なら logs_v3_1_test 下に出力）")

    args = parser.parse_args()

    source = args.source
    if not os.path.isdir(source):
        print(f"[ERROR] ソースディレクトリが存在しません: {source}")
        sys.exit(2)

    outdir = args.output or "logs_v3_1_test"
    os.makedirs(outdir, exist_ok=True)

    # exceptions 出力先
    exceptions_dir = os.path.join(outdir, "exceptions")
    os.makedirs(exceptions_dir, exist_ok=True)

    html_files = sorted(f for f in os.listdir(source) if f.endswith(".html"))
    if not html_files:
        print("[WARN] HTML ファイルが見つかりません")
        sys.exit(0)

    # 全ファイル処理
    for fname in html_files:
        fpath = os.path.join(source, fname)
        law_id = extract_law_id(fpath)

        result = validate_html_structure(fpath)

        # ログ書き込み
        write_json(
            os.path.join(exceptions_dir, f"{law_id}.json"),
            result
        )

    print("[INFO] validate 完了")
    sys.exit(0)


if __name__ == "__main__":
    main()
