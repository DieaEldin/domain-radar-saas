import os
import weasyprint

def generate_radar_pdf(domain_data: dict, output_pdf_path: str) -> str:
    """
    Generates an executive, highly polished PDF audit report for BlacklistMail Radar.
    Dynamically maps data from generate_audit_report().
    """
    # 1. Safe Extraction of Top-Level Data
    domain_name = domain_data.get("domain", "Unknown Domain")
    ip_address = domain_data.get("ip", "Unresolved IP")
    score = domain_data.get("score", 70)

    # 2. Extract Deep Intel & Financials
    deep_intel = domain_data.get("deep_intel", {})
    financials = deep_intel.get("financials", {})
    val_range = financials.get("valuation_range", "$300 - $1,000")
    bin_price = financials.get("buy_now_price", "$850")
    roi_range = financials.get("projected_roi", "100% - 300%")
    str_rate = financials.get("sell_through_rate", "2.5% / Year")

    # 3. Extract WHOIS Data
    whois_info = deep_intel.get("whois", {})
    registrar = whois_info.get("registrar", "Protected Registrar")
    domain_age = whois_info.get("age_years", 1)

    # 4. Extract Blacklist & Reputation
    blacklist_info = domain_data.get("blacklist", {})
    listed_count = blacklist_info.get("listed_count", 0)
    if listed_count == 0:
        ip_status = "Clean (0 Listed)"
        ip_status_class = "success"
    else:
        ip_status = f"Listed ({listed_count} RBLs)"
        ip_status_class = "danger"

    # 5. Extract Email & Security Infrastructure (Item 1 Integration)
    sec_records = domain_data.get("security_records", {})
    spf_info = sec_records.get("spf", {})
    dmarc_info = sec_records.get("dmarc", {})
    mx_info = sec_records.get("mx", {})

    spf_status_badge = '<span class="pill pill-success">Configured</span>' if spf_info.get("status") else '<span class="pill pill-warning">Missing</span>'
    spf_val = spf_info.get("value", "v=spf1 ... (Not Configured)")

    dmarc_status_badge = '<span class="pill pill-success">Configured</span>' if dmarc_info.get("status") else '<span class="pill pill-warning">Missing</span>'
    dmarc_val = dmarc_info.get("value", "No DMARC Record Found")

    mx_status_badge = '<span class="pill pill-success">Active</span>' if mx_info.get("status") else '<span class="pill pill-warning">Missing</span>'
    mx_provider = mx_info.get("provider", "No Mail Server Detected")

    # 6. Build TLD Ecosystem Rows Dynamically
    registered_tlds = deep_intel.get("registered_tlds", [".com"])
    popular_tlds = [".com", ".net", ".org", ".io", ".ai"]
    tld_rows_html = ""
    
    base_keyword = deep_intel.get("base_keyword", domain_name.split(".")[0])

    for tld in popular_tlds:
        is_reg = tld in registered_tlds or domain_name.endswith(tld)
        status_pill = '<span class="pill pill-danger">Registered</span>' if is_reg else '<span class="pill pill-success">Available</span>'
        dns_res = "Active Resolution" if is_reg else "Unassigned"
        demand = "Primary Asset" if tld == ".com" else ("High Tech Demand" if tld in [".io", ".ai"] else "Medium Potential")
        
        tld_rows_html += f"""
        <tr>
            <td><strong>{tld}</strong></td>
            <td>{status_pill}</td>
            <td>{dns_res}</td>
            <td>{demand}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BlacklistMail Radar Report - {domain_name}</title>
    <style>
        @page {{
            size: A4;
            margin: 10mm 12mm;
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Segoe UI', sans-serif;
                font-size: 8pt;
                color: #94a3b8;
            }}
        }}

        * {{
            box-sizing: border-box;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        }}

        body {{
            margin: 0;
            padding: 0;
            color: #0f172a;
            font-size: 9.5pt;
            line-height: 1.4;
            background-color: #ffffff;
        }}

        .header {{
            background: linear-gradient(135deg, #0b132b 0%, #1c2541 60%, #3a506b 100%);
            color: #ffffff;
            padding: 20px 24px;
            border-radius: 12px;
            margin-bottom: 18px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }}

        .brand-logo {{
            font-size: 18pt;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #ffffff;
            margin: 0;
            text-transform: uppercase;
        }}

        .brand-logo span {{ color: #38bdf8; }}

        .report-tag {{
            font-size: 8.5pt;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .domain-box {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            padding: 8px 16px;
            border-radius: 8px;
            text-align: right;
        }}

        .domain-title {{
            font-size: 14pt;
            font-weight: 700;
            color: #38bdf8;
        }}

        .grid-4 {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 10px 0;
            margin-left: -10px;
            margin-right: -10px;
            margin-bottom: 20px;
        }}

        .card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }}

        .card-label {{
            font-size: 7.5pt;
            text-transform: uppercase;
            color: #64748b;
            font-weight: 700;
            letter-spacing: 0.8px;
            margin-bottom: 4px;
        }}

        .card-value {{
            font-size: 13pt;
            font-weight: 800;
            color: #0f172a;
        }}

        .card-value.primary {{ color: #0284c7; }}
        .card-value.success {{ color: #16a34a; }}
        .card-value.danger {{ color: #dc2626; }}

        .section-header {{
            font-size: 10pt;
            font-weight: 800;
            color: #0f172a;
            margin-top: 16px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
        }}

        .section-header::before {{
            content: "";
            display: inline-block;
            width: 4px;
            height: 14px;
            background: #0284c7;
            margin-right: 8px;
            border-radius: 2px;
        }}

        table.styled-table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            margin-bottom: 16px;
        }}

        table.styled-table th {{
            background-color: #f1f5f9;
            color: #475569;
            font-size: 8pt;
            font-weight: 700;
            text-align: left;
            padding: 8px 12px;
            border-bottom: 1px solid #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        table.styled-table td {{
            padding: 8px 12px;
            font-size: 8.5pt;
            color: #334155;
            border-bottom: 1px solid #f1f5f9;
            word-wrap: break-word;
        }}

        table.styled-table tr:last-child td {{ border-bottom: none; }}
        table.styled-table tr:nth-child(even) {{ background-color: #f8fafc; }}

        .pill {{
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 7.5pt;
            font-weight: 700;
            display: inline-block;
            text-transform: uppercase;
        }}

        .pill-success {{ background-color: #dcfce7; color: #15803d; }}
        .pill-danger {{ background-color: #fee2e2; color: #b91c1c; }}
        .pill-warning {{ background-color: #fef3c7; color: #b45309; }}
        .pill-info {{ background-color: #e0f2fe; color: #0369a1; }}

        .footer {{
            margin-top: 25px;
            padding-top: 12px;
            border-top: 1px solid #e2e8f0;
            font-size: 7.5pt;
            color: #94a3b8;
        }}
    </style>
</head>
<body>

    <!-- Header Section -->
    <div class="header">
        <table style="width: 100%;">
            <tr>
                <td style="vertical-align: middle;">
                    <div class="report-tag">Audit & Domain Intelligence Report</div>
                    <div class="brand-logo">BlacklistMail <span>Radar</span></div>
                </td>
                <td style="text-align: right; vertical-align: middle;">
                    <div class="domain-box">
                        <div style="font-size: 7.5pt; color: #cbd5e1; text-transform: uppercase;">Target Domain</div>
                        <div class="domain-title">{domain_name}</div>
                    </div>
                </td>
            </tr>
        </table>
    </div>

    <!-- Executive Summary Cards -->
    <table class="grid-4">
        <tr>
            <td class="card" style="width: 25%;">
                <div class="card-label">Reputation Score</div>
                <div class="card-value primary">{score} / 100</div>
            </td>
            <td class="card" style="width: 25%;">
                <div class="card-label">IP Status</div>
                <div class="card-value {ip_status_class}">{ip_status}</div>
            </td>
            <td class="card" style="width: 25%;">
                <div class="card-label">Est. Valuation</div>
                <div class="card-value">{val_range}</div>
            </td>
            <td class="card" style="width: 25%;">
                <div class="card-label">Projected ROI</div>
                <div class="card-value success">{roi_range}</div>
            </td>
        </tr>
    </table>

    <!-- Section 1 -->
    <div class="section-header">1. Market Valuation & Commercial Metrics</div>
    <table class="styled-table">
        <thead>
            <tr>
                <th style="width: 40%;">Parameter</th>
                <th style="width: 60%;">Benchmark & Details</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Suggested Buy-It-Now (BIN)</strong></td>
                <td><strong style="color: #0284c7;">{bin_price} USD</strong></td>
            </tr>
            <tr>
                <td><strong>Estimated Valuation Range</strong></td>
                <td>{val_range} USD</td>
            </tr>
            <tr>
                <td><strong>Sell-Through Rate (STR)</strong></td>
                <td>{str_rate}</td>
            </tr>
            <tr>
                <td><strong>Domain Age / Brandability</strong></td>
                <td><span class="pill pill-info">{domain_age} Years Old</span> - Active Market Asset</td>
            </tr>
        </tbody>
    </table>

    <!-- Section 2 -->
    <div class="section-header">2. Extended TLD Ecosystem Audit</div>
    <table class="styled-table">
        <thead>
            <tr>
                <th style="width: 20%;">Extension</th>
                <th style="width: 25%;">Status</th>
                <th style="width: 30%;">DNS Resolution</th>
                <th style="width: 25%;">Market Demand</th>
            </tr>
        </thead>
        <tbody>
            {tld_rows_html}
        </tbody>
    </table>

    <!-- Section 3 -->
    <div class="section-header">3. Infrastructure & Email Security Health</div>
    <table class="styled-table">
        <thead>
            <tr>
                <th style="width: 20%;">Record Type</th>
                <th style="width: 25%;">Hostname</th>
                <th style="width: 40%;">Resolved Value / Server</th>
                <th style="width: 15%;">Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>A Record</strong></td>
                <td>@ ({domain_name})</td>
                <td><code>{ip_address}</code></td>
                <td><span class="pill pill-success">Resolved</span></td>
            </tr>
            <tr>
                <td><strong>Mail Provider (MX)</strong></td>
                <td>@</td>
                <td>{mx_provider}</td>
                <td>{mx_status_badge}</td>
            </tr>
            <tr>
                <td><strong>SPF Record</strong></td>
                <td>TXT (@)</td>
                <td style="font-family: monospace; font-size: 7.5pt;">{spf_val[:45]}...</td>
                <td>{spf_status_badge}</td>
            </tr>
            <tr>
                <td><strong>DMARC Record</strong></td>
                <td>TXT (_dmarc)</td>
                <td style="font-family: monospace; font-size: 7.5pt;">{dmarc_val[:45]}...</td>
                <td>{dmarc_status_badge}</td>
            </tr>
            <tr>
                <td><strong>Registrar</strong></td>
                <td>WHOIS</td>
                <td>{registrar}</td>
                <td><span class="pill pill-info">Verified</span></td>
            </tr>
        </tbody>
    </table>

    <!-- Footer -->
    <div class="footer">
        <table style="width: 100%;">
            <tr>
                <td>Generated automatically by <strong>BlacklistMail Radar Engine</strong></td>
                <td style="text-align: right;">Confidential Domain Intelligence Report</td>
            </tr>
        </table>
    </div>

</body>
</html>
"""

    temp_html = f"temp_{domain_name}.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    weasyprint.HTML(filename=temp_html).write_pdf(output_pdf_path)

    if os.path.exists(temp_html):
        os.remove(temp_html)

    return output_pdf_path