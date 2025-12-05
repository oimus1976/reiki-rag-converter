"""
synthetic_generator_v0_1.py

synthetic HTML を自動生成する最初のバージョン。
とりあえず以下のパターンのみ対応する：

- P1: 基本構造（最小）
- P2: 用語定義型（項・号）
- P3: 本則内の表（table）

P4 以降は TODO とし、段階的に実装を追加していく。
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import argparse
import json
from datetime import date


ROOT = Path(__file__).resolve().parents[1]
SYN_HTML_DIR = ROOT / "synthetic_html"
SYN_META_DIR = ROOT / "synthetic_html_meta"


# ---------------------------------------------------------
# データクラス
# ---------------------------------------------------------

@dataclass
class SyntheticMeta:
    law_id: str
    pattern: str
    title: str
    article_count: int
    has_items: bool
    has_table_main: bool
    has_table_supplement: bool
    supplement_count: int
    nested_div: bool = False
    s_head_style: str = "A"
    inline_depth: int = 1
    table_wrapper: str = "normal"
    anomalies: Optional[list] = None

    def to_dict(self) -> dict:
        return {
            "law_id": self.law_id,
            "pattern": self.pattern,
            "title": self.title,
            "structure": {
                "article_count": self.article_count,
                "has_items": self.has_items,
                "has_table_main": self.has_table_main,
                "has_table_supplement": self.has_table_supplement,
                "supplement_count": self.supplement_count,
            },
            "dom_variation": {
                "nested_div": self.nested_div,
                "s_head_style": self.s_head_style,
                "inline_depth": self.inline_depth,
                "table_wrapper": self.table_wrapper,
            },
            "anomalies": self.anomalies or [],
            "created_at": date.today().isoformat(),
        }


# ---------------------------------------------------------
# パターン別 HTML テンプレ
# ---------------------------------------------------------

def build_html_p1(meta: SyntheticMeta) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{meta.title}</title>
  <link rel="stylesheet" href="reiki.css">
</head>
<body>
<div id="wrapper">
  <div id="container">
    <div id="primary" class="joubun showhistory">
      <div id="primaryInner">
        <div id="primaryInner2">

          <div class="eline">
            <p class="title">{meta.title}</p>
          </div>
          <div class="eline">
            <p class="date">令和5年4月1日</p>
          </div>
          <div class="eline">
            <p class="number">条例第1号</p>
          </div>

          <div class="eline">
            <div class="article">
              <p class="num">（目的）</p>
              <p>第1条　この条例は、サンプル町における基本的な事項を定めることを目的とする。</p>
            </div>
          </div>

          <div class="eline">
            <div class="article">
              <p class="num">（委任）</p>
              <p>第2条　この条例の施行に関し必要な事項は、規則で定める。</p>
            </div>
          </div>

          <div class="eline">
            <p class="s-head">
              <span class="title">附則</span>
              <span class="date">（令和5年4月1日 条例第1号）</span>
            </p>
          </div>
          <div class="eline">
            <div class="article">
              <p>１　この条例は、公布の日から施行する。</p>
            </div>
          </div>

        </div>
      </div>
    </div>
    <div id="secondary"></div>
  </div>
</div>
</body>
</html>
"""


def build_html_p2(meta: SyntheticMeta) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{meta.title}</title>
  <link rel="stylesheet" href="reiki.css">
</head>
<body>
<div id="wrapper">
  <div id="container">
    <div id="primary" class="joubun showhistory">
      <div id="primaryInner">
        <div id="primaryInner2">

          <div class="eline">
            <p class="title">{meta.title}</p>
          </div>
          <div class="eline">
            <p class="date">令和5年4月1日</p>
          </div>
          <div class="eline">
            <p class="number">条例第2号</p>
          </div>

          <div class="eline">
            <div class="article">
              <p class="num">（目的）</p>
              <p>第1条　この条例は、用語の定義その他必要な事項を定めることを目的とする。</p>
            </div>
          </div>

          <div class="eline">
            <div class="article">
              <p class="num">（定義）</p>
              <div class="clause">
                <p>第2条　この条例において「情報システム」とは、サンプル町が業務のために利用する機器及びサービスの総体をいう。</p>
                <div class="item">
                  <p class="num">(1)</p>
                  <p>サーバ　町の業務データを保存し、又は処理する装置をいう。</p>
                </div>
                <div class="item">
                  <p class="num">(2)</p>
                  <p>クライアント　職員が日常の事務のために使用する端末をいう。</p>
                </div>
              </div>
            </div>
          </div>

          <div class="eline">
            <p class="s-head">
              <span class="title">附則</span>
              <span class="date">（令和5年4月1日 条例第2号）</span>
            </p>
          </div>
          <div class="eline">
            <div class="article">
              <p>１　この条例は、公布の日から施行する。</p>
            </div>
          </div>

        </div>
      </div>
    </div>
    <div id="secondary"></div>
  </div>
</div>
</body>
</html>
"""


def build_html_p3(meta: SyntheticMeta) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{meta.title}</title>
  <link rel="stylesheet" href="reiki.css">
</head>
<body>
<div id="wrapper">
  <div id="container">
    <div id="primary" class="joubun showhistory">
      <div id="primaryInner">
        <div id="primaryInner2">

          <div class="eline">
            <p class="title">{meta.title}</p>
          </div>
          <div class="eline">
            <p class="date">令和5年4月1日</p>
          </div>
          <div class="eline">
            <p class="number">条例第3号</p>
          </div>

          <div class="eline">
            <div class="article">
              <p class="num">（駐車料金）</p>
              <p>第1条　サンプル町が設置する駐車場の使用料は、次の表のとおりとする。</p>
            </div>
          </div>

          <div class="eline">
            <div class="table_frame">
              <div class="table-wrapper">
                <table class="b-on">
                  <thead>
                    <tr>
                      <th>区分</th>
                      <th>料金</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>普通自動車</td>
                      <td>1時間につき 100円</td>
                    </tr>
                    <tr>
                      <td>大型自動車</td>
                      <td>1時間につき 200円</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="eline">
            <p class="s-head">
              <span class="title">附則</span>
              <span class="date">（令和5年4月1日 条例第3号）</span>
            </p>
          </div>
          <div class="eline">
            <div class="article">
              <p>１　この条例は、公布の日から施行する。</p>
            </div>
          </div>

        </div>
      </div>
    </div>
    <div id="secondary"></div>
  </div>
</div>
</body>
</html>
"""


# ---------------------------------------------------------
# 生成ディスパッチ
# ---------------------------------------------------------

def generate_html_and_meta(pattern: str, law_id: str, title: str) -> None:
    SYN_HTML_DIR.mkdir(parents=True, exist_ok=True)
    SYN_META_DIR.mkdir(parents=True, exist_ok=True)

    if pattern == "P1":
        meta = SyntheticMeta(
            law_id=law_id,
            pattern="P1",
            title=title,
            article_count=2,
            has_items=False,
            has_table_main=False,
            has_table_supplement=False,
            supplement_count=1,
        )
        html = build_html_p1(meta)
    elif pattern == "P2":
        meta = SyntheticMeta(
            law_id=law_id,
            pattern="P2",
            title=title,
            article_count=2,
            has_items=True,
            has_table_main=False,
            has_table_supplement=False,
            supplement_count=1,
        )
        html = build_html_p2(meta)
    elif pattern == "P3":
        meta = SyntheticMeta(
            law_id=law_id,
            pattern="P3",
            title=title,
            article_count=1,
            has_items=False,
            has_table_main=True,
            has_table_supplement=False,
            supplement_count=1,
        )
        html = build_html_p3(meta)
    else:
        raise ValueError(f"Unsupported pattern for v0.1: {pattern}")

    html_path = SYN_HTML_DIR / f"{law_id}_{pattern}.html"
    meta_path = SYN_META_DIR / f"{law_id}.json"

    html_path.write_text(html, encoding="utf-8")
    meta_path.write_text(json.dumps(meta.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic HTML for reiki-rag-converter (v0.1).")
    parser.add_argument("--pattern", required=True, choices=["P1", "P2", "P3"], help="Synthetic pattern ID")
    parser.add_argument("--law-id", required=True, help="Synthetic law ID, e.g., synRG00000001")
    parser.add_argument("--title", required=True, help="Title of the synthetic law")
    args = parser.parse_args()

    generate_html_and_meta(args.pattern, args.law_id, args.title)


if __name__ == "__main__":
    main()
