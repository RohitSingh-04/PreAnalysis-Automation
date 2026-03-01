import pandas as pd
import numpy as np
import html
from datetime import datetime
from app import url_generator

def top_counterparties_to_html(
    top_counterparties: pd.DataFrame,
    title: str = "Top Counterparties by Triggered Rule",
    currency_symbol: str = "$",
    table_id_prefix: str = "rule",
) -> str:
    """
    Renders separate HTML sections per triggered rule (uses 'Alert Information').

    Expected columns:
      - Alert Information (rule text)
      - Counterparty
      - Total Amount
    """
    df = top_counterparties.copy()

    required = ["Alert Information", "Counterparty", "Total Amount"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found: {list(df.columns)}")

    # Ensure numeric + consistent ordering
    df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors="coerce")
    df = df.sort_values(["Alert Information", "Total Amount"], ascending=[True, False]).reset_index(drop=True)

    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    sections = []
    for i, (rule, g) in enumerate(df.groupby("Alert Information", dropna=False), start=1):
        rule_display = "" if pd.isna(rule) else str(rule)

        # Format display amounts
        g = g.copy()
        g["Total Amount (formatted)"] = g["Total Amount"].map(
            lambda x: "" if pd.isna(x) else f"{currency_symbol}{x:,.2f}"
        )

        # Build rows
        rows_html = []
        
        for _, r in g.iterrows():
            if not pd.isna(r['Counterparty']):
              urls = [html.escape(url_generator.google_search_url(str(r['Counterparty']))), 
                      html.escape(url_generator.google_string_search_url(str(r['Counterparty'])))]
              
              url_text = "Click Here"

            else:
              urls = ["", ""]
              url_text = ""

            rows_html.append(
                "<tr>\n"
                f"<td>{html.escape(str(r['Counterparty']))}</td>\n"
                f"<td class='num'>{html.escape(str(r['Total Amount (formatted)']))}</td>\n"
                f"<td> <a href=\"{urls[0]}\" target=\"_blank\">{url_text}</a></td>\n"
                f"<td> <a href=\"{urls[1]}\" target=\"_blank\">{url_text}</a></td>\n"
                "</tr>"
            )
            
        rows_html = "\n".join(rows_html)

        safe_id = f"{table_id_prefix}-{i}"
        sections.append(
            f"""
<section class="rule-section">
  <h2 class="rule-title">{html.escape(rule_display)}</h2>
  <p class="rule-meta">Counterparties shown: {len(g)}</p>
  <table id="{html.escape(safe_id)}" aria-label="{html.escape(rule_display)}">
    <thead>
      <tr>
        <th>Counterparty</th>
        <th>Total Amount</th>
        <th>Google Search</th>
        <th>Negative News Search</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</section>
""".strip()
        )

    sections_html = "\n\n".join(sections)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Arial, Helvetica, sans-serif; margin: 24px; color: #1a1a1a; }}
    h1 {{ font-size: 18px; margin: 0 0 6px 0; }}
    .meta {{ font-size: 12px; color: #555; margin: 0 0 18px 0; }}
    .rule-section {{ margin: 18px 0 26px 0; }}
    .rule-title {{ font-size: 15px; margin: 0 0 6px 0; }}
    .rule-meta {{ font-size: 12px; color: #555; margin: 0 0 10px 0; }}

    table {{ border-collapse: collapse; width: 100%; max-width: 980px; }}
    th, td {{ border: 1px solid #ddd; padding: 10px 12px; font-size: 13px; }}
    th {{ background: #f6f6f6; text-align: left; }}
    td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    tbody tr:nth-child(even) {{ background: #fbfbfb; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p class="meta">Rows: {len(df)} &bull; Generated: {generated_at}</p>

  {sections_html}
</body>
</html>"""


def detect_counterparty(df: pd.DataFrame, output_dir: str):

    df["Transaction Amount"] = pd.to_numeric(df["Transaction Amount"], errors="coerce")

    df["Counterparty"] = np.where(
        df["Dr Cr"].str.upper().eq("DR"),
        df["Beneficiary Name"],
        df["Originator Name"],
    )

    top_n = 4

    top_counterparties = (
        df.groupby(["Alert Information", "Counterparty"], dropna=False)["Transaction Amount"]
        .sum()
        .reset_index(name="Total Amount")
        .sort_values(["Alert Information", "Total Amount"], ascending=[True, False])
    )

    top_counterparties = top_counterparties.groupby("Alert Information").head(top_n).reset_index(drop=True)

    with open(output_dir, "w") as fh:
        fh.write(top_counterparties_to_html(top_counterparties))

    cntrsptys = top_counterparties["Counterparty"].dropna()

    return cntrsptys