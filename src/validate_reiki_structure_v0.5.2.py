"""
validate_reiki_structure_v0.5.2 (GitHub整形版)
-------------------------------------------------------
例規HTML（reiki_honbun/*.html）の DOM 構造を検証し、
条・項・号・附則・表などの出現、および例外(E系)を検出する。

出力:
    logs_v3_1/exceptions/{LAW_ID}.json
    logs_v3_1/summary_report.json
    logs_v3_1/class_statistics.json
    logs_v3_1/structure_summary.json   ← v3.1 の新機能

※ 元コード v0.5.2 のロジックを保持しつつ、
   GitHub 用に可読性・構造性を強化した整形版。
"""

import os
import argparse
import json
import chardet
from bs4 import BeautifulSoup

# ============================================================
# E 系（例外コード）
# ============================================================
"""
E001: 未知class
E003: 公布日欠落
E004: 条例番号欠落
E007: #primaryInner2 欠落
E006X: 表/リストの異常配置（将来拡張）
"""

# ============================================================
# S 系（構造イベントコード）
# ============================================================
"""
S1: table_in_main         本則中の表
S2: table_in_supplement   附則中の表
S3: ul_in_item            リスト構造
"""

# ============================================================
# 既知クラス一覧（元 v2 仕様）
# ============================================================
KNOWN_CLASSES = {
    "eline", "article", "clause", "item", "num", "title",
    "title-irregular", "date", "number", "p", "s-head",
    "table_frame", "table-wrapper",
    "b-on", "bb-on", "br-on",
    "l-edge", "r-edge", "t-edge", "b-edge",
    "fixed-colspec",
    "inline", "quote", "xref_frame",
    "cm", "word-space", "top", "start",
    "none", "close", "open", "noicon",
    "main_rules", "supplement"
}

# ============================================================
# エンコーディング付き HTML 読込
# ============================================================
def read_html(path: str) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    enc = chardet.detect(raw)["encoding"] or "utf-8"
    try:
        return raw.decode(enc, errors="ignore")
    except Exception:
        return raw.decode("utf-8", errors="ignore")


# ============================================================
# 公布日 / 番号 の検出（簡易チェック）
# ============================================================
def detect_basic_meta(main) -> tuple[bool, bool]:
    """公布日(date)・番号(number)が存在するかの真偽を返す"""
    has_date = bool(main.select_one("p.date"))
    has_number = bool(main.select_one("p.number"))
    return has_date, has_number


# ============================================================
# 例外クラス E001 の検出（.eline 内の未知 class）
# ============================================================
def collect_unknown_classes(eline) -> list[str]:
    found = []
    for tag in eline.find_all(True):
        for c in tag.get("class", []):
            if c not in KNOWN_CLASSES:
                found.append(c)
    return found


# ============================================================
# 構造イベント（S系）の検出
# ============================================================
def detect_structure_events(eline, in_supplement: bool) -> list[dict]:
    structures = []

    # table 検出
    if eline.find("table"):
        if in_supplement:
            structures.append({"event": "table_in_supplement"})
        else:
            structures.append({"event": "table_in_main"})

    # ul/li 検出
    if eline.find("ul") or eline.find("li"):
        structures.append({"event": "ul_in_item"})

    return structures


# ============================================================
# 1ファイルの解析
# ============================================================
def analyze_html(path: str) -> dict:
    html = read_html(path)
    soup = BeautifulSoup(html, "html.parser")

    result = {
        "exceptions": [],
        "structures": [],
        "classes": set()
    }

    main = soup.select_one("#primaryInner2")
    if not main:
        result["exceptions"].append("E007")
        return result

    # 公布日・番号
    has_date, has_number = detect_basic_meta(main)
    if not has_date:
        result["exceptions"].append("E003")
    if not has_number:
        result["exceptions"].append("E004")

    elines = main.select(".eline")
    in_supplement = False

    for idx, el in enumerate(elines):
        # class収集
        for tag in el.find_all(True):
            for c in tag.get("class", []):
                result["classes"].add(c)
                if c not in KNOWN_CLASSES:
                    result["exceptions"].append("E001")

        # 附則判定
        if "s-head" in el.get("class", []):
            in_supplement = True

        # Sイベント
        events = detect_structure_events(el, in_supplement)
        for ev in events:
            ev["index"] = idx
            result["structures"].append(ev)

    # 重複削除
    result["exceptions"] = sorted(set(result["exceptions"]))
    result["classes"] = sorted(result["classes"])

    return result


# ============================================================
# 全条例の集計処理
# ============================================================
def summarize_all_logs(logs: dict):
    """
    logs: { law_id: per-law JSON }
    """
    summary_exceptions = {}
    class_statistics = {}
    structure_summary = {}

    for law_id, data in logs.items():

        # --- exceptions 集計 ---
        for ex in data["exceptions"]:
            summary_exceptions.setdefault(ex, []).append(law_id)

        # --- classes 集計 ---
        for c in data["classes"]:
            class_statistics[c] = class_statistics.get(c, 0) + 1

        # --- structures 集計 ---
        for st in data["structures"]:
            ev = st["event"]
            idx = st["index"]

            if ev not in structure_summary:
                structure_summary[ev] = {"count": 0, "laws": []}

            structure_summary[ev]["count"] += 1

            # 1条例単位で index 群をまとめる
            if (not structure_summary[ev]["laws"]) or \
               (structure_summary[ev]["laws"][-1]["id"] != law_id):
                structure_summary[ev]["laws"].append({
                    "id": law_id, "indexes": [idx]
                })
            else:
                structure_summary[ev]["laws"][-1]["indexes"].append(idx)

    return {
        "summary_exceptions": summary_exceptions,
        "class_statistics": class_statistics,
        "structure_summary": structure_summary
    }


# ============================================================
# ファイル保存
# ============================================================
def write_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# メイン処理
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Validate structure of Reiki HTML files."
    )
    parser.add_argument(
        "--source",
        "-s",
        default="reiki_honbun",
        help="HTMLファイルを含むディレクトリ"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="logs_v3_1",
        help="ログ出力先ディレクトリ（デフォルト: logs_v3_1）"
    )
    args = parser.parse_args()

    source = args.source
    output_dir = args.output
    exceptions_dir = os.path.join(output_dir, "exceptions")

    files = sorted(f for f in os.listdir(source) if f.endswith(".html"))

    all_logs = {}

    for fname in files:
        path = os.path.join(source, fname)
        law_id = fname.replace(".html", "")
        res = analyze_html(path)

        # 個別ログ
        write_json(os.path.join(exceptions_dir, f"{law_id}.json"), res)

        all_logs[law_id] = res
        print(f"[OK] analyzed {law_id}")

    # サマリー出力
    summary = summarize_all_logs(all_logs)

    write_json(os.path.join(output_dir, "summary_report.json"),
               summary["summary_exceptions"])
    write_json(os.path.join(output_dir, "class_statistics.json"),
               summary["class_statistics"])
    write_json(os.path.join(output_dir, "structure_summary.json"),
               summary["structure_summary"])

    print("\n=== DONE ===")
    print(f"Logs saved to: {output_dir}")


if __name__ == "__main__":
    main()
