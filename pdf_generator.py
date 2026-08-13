import os
import weasyprint

def generate_radar_pdf(domain_data: dict, output_pdf_path: str) -> str:
    """
    Generates an executive, highly polished PDF audit report for BlacklistMail Radar.
    """
    domain_name = domain_data.get("domain", "example.com")
    val_low = domain_data.get("val_low", "$864")
    val_high = domain_data.get("val_high", "$1,475")
    bin_price = domain_data.get("bin_price", "$1,170 USD")
    roi_range = domain_data.get("roi_range", "7,100% - 12,191%")
    str_rate = domain_data.get("str_rate", "3.7% / Year")
    ip_status = domain_data.get("ip_status", "Clean (0 Listed)")
    ip_address = domain_data.get("ip_address", "216.24.57.1")
    registrar = domain_data.get("registrar", "Dynadot LLC")
    score = domain_data.get("score", "9.8")

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

        /* Top Header Component */
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

        .brand-logo span {{
            color: #38bdf8;
        }}

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

        /* Key Performance Grid */
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
            font-size: 14pt;
            font-weight: 800;
            color: #0f172a;
        }}

        .card-value.primary {{ color: #0284c7; }}
        .card-value.success {{ color: #16a34a; }}
        .card-value.warning {{ color: #d97706; }}

        /* Section Title Styling */
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

        /* Tables */
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
        }}

        table.styled-table tr:last-child td {{ border-bottom: none; }}
        table.styled-table tr:nth-child(even) {{ background-color: #f8fafc; }}

        /* Status Pills */
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

        /* Footer */
        .footer {{
            margin-top: 25px;
            padding-top: 12px;
            border-top: 1px solid #e2e8f0;
            text-align: space-between;
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
                <div class="card-value success">{ip_status}</div>
            </td>
            <td class="card" style="width: 25%;">
                <div class="card-label">Est. Valuation</div>
                <div class="card-value">{val_high}</div>
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
                <td><strong style="color: #0284c7;">{bin_price}</strong></td>
            </tr>
            <tr>
                <td><strong>Estimated Valuation Range</strong></td>
                <td>{val_low} - {val_high} USD</td>
            </tr>
            <tr>
                <td><strong>Sell-Through Rate (STR)</strong></td>
                <td>{str_rate}</td>
            </tr>
            <tr>
                <td><strong>Brandability Score</strong></td>
                <td><span class="pill pill-info">High (9.5 / 10)</span> - Category Exact Match</td>
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
            <tr>
                <td><strong>.com</strong></td>
                <td><span class="pill pill-danger">Registered</span></td>
                <td>Active (Render Cloud)</td>
                <td>Primary Asset</td>
            </tr>
            <tr>
                <td><strong>.net</strong></td>
                <td><span class="pill pill-success">Available</span></td>
                <td>Unassigned</td>
                <td>Medium Potential</td>
            </tr>
            <tr>
                <td><strong>.org</strong></td>
                <td><span class="pill pill-success">Available</span></td>
                <td>Unassigned</td>
                <td>Medium Potential</td>
            </tr>
            <tr>
                <td><strong>.io</strong></td>
                <td><span class="pill pill-success">Available</span></td>
                <td>Unassigned</td>
                <td>High SaaS Demand</td>
            </tr>
            <tr>
                <td><strong>.ai</strong></td>
                <td><span class="pill pill-success">Available</span></td>
                <td>Unassigned</td>
                <td>High Tech Demand</td>
            </tr>
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
                <td><span class="pill pill-success">Active</span></td>
            </tr>
            <tr>
                <td><strong>CNAME</strong></td>
                <td>www.{domain_name}</td>
                <td><code>domain-radar-saas.onrender.com</code></td>
                <td><span class="pill pill-success">Active</span></td>
            </tr>
            <tr>
                <td><strong>MX Record</strong></td>
                <td>@</td>
                <td><em>No Mail Server Detected</em></td>
                <td><span class="pill pill-warning">Missing</span></td>
            </tr>
            <tr>
                <td><strong>SPF Record</strong></td>
                <td>TXT (@)</td>
                <td><em>v=spf1 ... (Not Configured)</em></td>
                <td><span class="pill pill-warning">Missing</span></td>
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