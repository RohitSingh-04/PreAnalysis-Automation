import html
import pandas as pd
from datetime import datetime
from app import url_generator

def customer_osdd_to_html(customer_names, customer_addresses, title="Customer Searches", generated_at=None):
    if generated_at is None:
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sections = []
    rows_html = []
    
    for customer_name in customer_names:
        for customer_address in customer_addresses:
            rows_html.append(
                "<tr>\n"
                f"<td>{customer_name}</td>\n"
                f"<td class='num'>{customer_address}</td>\n"
                f"<td> <a href=\"{html.escape(url_generator.google_search_url(str(customer_name)))}\" target=\"_blank\">Click Here</a></td>\n"
                f"<td> <a href=\"{html.escape(url_generator.google_search_url(str(customer_address)))}\" target=\"_blank\">Click Here</a></td>\n"
                f"<td> <a href=\"{html.escape(url_generator.google_name_address_url(str(customer_name),str(customer_address)))}\" target=\"_blank\">Click Here</a></td>\n"
                f"<td> <a href=\"{html.escape(url_generator.google_string_search_url(str(customer_name)))}\" target=\"_blank\">Click Here</a></td>\n"
                "</tr>"
            )
            
    rows_html = "\n".join(rows_html)
    
    sections.append(
        f"""
<section class="rule-section">
  <h2 class="rule-title">Customer Searches</h2>
  <table aria-label="Customer Details">
    <thead>
      <tr>
        <th>Customer Varient</th>
        <th>Address Varient</th>
        <th>Google Search</th>
        <th>Address Search</th>
        <th>Google + Address Search</th>
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
  <p class="meta">Generated: {generated_at}</p>

  {sections_html}
</body>
</html>"""


def detect_customer(df:pd.DataFrame, output_dir:str):
    
    CUSTOMER = {0: "Beneficiary Name", 1: "Originator Name"}
    ADDRESS = {0: "Beneficiary Address", 1: 'Originator Address'}
    
    customer_variants = set()
    customer_address_variants = set()
    
    df_credits = df[df['Dr Cr'] == "CR"]
    df_debits = df[df['Dr Cr'] == "DR"]
    
    customer_variants.update(df_credits[CUSTOMER[0]].unique())
    customer_variants.update(df_debits[CUSTOMER[1]].unique())
    
    customer_address_variants.update(df_credits[ADDRESS[0]].unique())
    customer_address_variants.update(df_debits[ADDRESS[1]].unique())
    
    html = customer_osdd_to_html(customer_variants, customer_address_variants)
    with open(output_dir, "w") as fh:
        fh.write(html)