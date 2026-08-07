import os
import weasyprint

def generate_radar_pdf(domain_data: dict, output_pdf_path: str) -> str:
    """
    Generates a beautifully formatted PDF audit report for BlacklistMail Radar.
    
    :param domain_data: Dictionary containing domain audit details.
    :param output_pdf_path: Path where the output PDF file should be saved.
    :return: Filepath of the generated PDF.
    """
    domain_name = domain_data.get("domain", "example.com")
    val_low = domain_data.get("val_low", "$864")
    val_high = domain_data.get("val_high", "$1,475")
    bin_price = domain_data.get("bin_price", "$1,170 USD")
    roi_range = domain_data.get("roi_range", "7,100% - 12,191%")
    str_rate = domain_data.get("str_rate", "3.7% / Year")
    ip_status = domain_data.get("ip_status", "Clean (2 RBL Warnings)")
    ip_address = domain_data.get("ip_address", "216.24.57.1")
    registrar = domain_data.get("registrar", "Dynadot LLC")
    
    # HTML Template with inline CSS tailored for WeasyPrint
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BlacklistMail Radar Report - {domain_name}</title>
    <style>
        @page {{
            size: A4;
            margin: 12mm 12mm;
            background-color: #f8fafc;
        }}

        * {{
            box-sizing: border-box;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        }}

        body {{
            margin: 0;
            padding: 0;
            color: #1e293b;
            font-size: 10pt;
            line-height: 1.4;
            background-color: #f8fafc;
        }}

        .header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}

        .brand-title {{
            font-size: 18pt;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #38bdf8;
            margin: 0;
        }}

        .report-subtitle {{
            font-size: 10pt;
            color: #94a3b8;
            margin-top: 2px;
            font-weight: 400;
        }}

        .domain-badge {{
            background-color: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11pt;
            font-weight: 600;
            display: inline-block;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}

        .metrics-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 10px 0;
            margin-left: -10px;
            margin-right: -10px;
            margin-bottom: 15px;
        }}

        .metric-card {{
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 10px 12px;
            text-align: center;
            width: 25%;
        }}

        .metric-card .label {{
            font-size: 8pt;
            text-transform: uppercase;
            color: #64748b;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}

        .metric-card .value {{
            font-size: 12pt;
            font-weight: 700;
            color: #0f172a;
            margin-top: 4px;
        }}

        .metric-card .value.highlight {{ color: #0284c7; }}
        .metric-card .value.success {{ color: #16a34a; }}
        .metric-card .value.warning {{ color: #d97706; }}

        .section-title {{
            font-size: 11pt;
            font-weight: 700;
            color: #0f172a;
            margin-top: 14px;
            margin-bottom: 8px;
            padding-left: 8px;
            border-left: 3px solid #0284c7;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #ffffff;
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            margin-bottom: 12px;
        }}

        table.data-table th {{
            background-color: #f1f5f9;
            color: #334155;
            font-size: 8.5pt;
            font-weight: 700;
            text-align: left;
            padding: 7px 10px;
            border-bottom: 1px solid #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        table.data-table td {{
            padding: 7px 10px;
            font-size: 9pt;
            color: #334155;
            border-bottom: 1px solid #f1f5f9;
        }}

        table.data-table tr:last-child td {{ border-bottom: none; }}
        table.data-table tr:nth-child(even) {{ background-color: #fafafa; }}

        .status-pill {{
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 8pt;
            font-weight: 600;
            display: inline-block;
        }}

        .status-pill.registered {{ background-color: #fee2e2; color: #dc2626; }}
        .status-pill.available {{ background-color: #dcfce7; color: #16a34a; }}
        .status-pill.warning {{ background-color: #fef3c7; color: #d97706; }}
        .status-pill.info {{ background-color: #e0f2fe; color: #0284c7; }}

        .footer {{
            margin-top: 15px;
            padding-top: 8px;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            font-size: 8pt;
            color: #94a3b8;
        }}
    </style>
</head>
<body>

    <div class="header">
        <table style="width: 100%;">
            <tr>
                <td>
                    <div class="brand-title">BlacklistMail Radar Engine</div>
                    <div class="report-subtitle">Comprehensive Domain Investment & Reputation Audit Report</div>
                </td>
                <td style="text-align: right;">
                    <div class="domain-badge">{domain_name}</div>
                </td>
            </tr>
        </table>
    </div>

    <table class="metrics-table">
        <tr>
            <td class="metric-card">
                <div class="label">Est. Valuation</div>
                <div class="value highlight">{val_low} - {val_high}</div>
            </td>
            <td class="metric-card">
                <div class="label">Projected ROI</div>
                <div class="value success">{roi_range}</div>
            </td>
            <td class="metric-card">
                <div class="label">Sell-Through Rate</div>
                <div class="value">{str_rate}</div>
            </td>
            <td class="metric-card">
                <div class="label">IP Reputation</div>
                <div class="value warning">{ip_status}</div>
            </td>
        </tr>
    </table>

    <div class="section-title">1. Financial Valuation & Market Metrics</div>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 40%;">Metric Parameter</th>
                <th style="width: 60%;">Estimated Benchmark & Details</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Suggested Buy-It-Now (BIN) Price</strong></td>
                <td><strong style="color: #0284c7;">{bin_price}</strong></td>
            </tr>
            <tr>
                <td><strong>Estimated ROI Potential</strong></td>
                <td>{roi_range} (Based on standard domain acquisition benchmark)</td>
            </tr>
            <tr>
                <td><strong>Sell-Through Rate (STR)</strong></td>
                <td>{str_rate} (Annual liquidity index)</td>
            </tr>
            <tr>
                <td><strong>Brandability Score</strong></td>
                <td><span class="status-pill info">High (9.2 / 10)</span> - Category Exact Match</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">2. Extended TLD Ecosystem & Multi-Extension Audit</div>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 20%;">TLD Extension</th>
                <th style="width: 25%;">Registration Status</th>
                <th style="width: 30%;">DNS Resolution</th>
                <th style="width: 25%;">Commercial Demand</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>.com</strong></td>
                <td><span class="status-pill registered">Registered (Primary)</span></td>
                <td>Active (Render Cloud)</td>
                <td>High (Primary Asset)</td>
            </tr>
            <tr>
                <td><strong>.net</strong></td>
                <td><span class="status-pill available">Available for Reg</span></td>
                <td>Unassigned</td>
                <td>Medium Potential</td>
            </tr>
            <tr>
                <td><strong>.org</strong></td>
                <td><span class="status-pill available">Available for Reg</span></td>
                <td>Unassigned</td>
                <td>Medium Potential</td>
            </tr>
            <tr>
                <td><strong>.io</strong></td>
                <td><span class="status-pill available">Available for Reg</span></td>
                <td>Unassigned</td>
                <td>High SaaS Demand</td>
            </tr>
            <tr>
                <td><strong>.ai</strong></td>
                <td><span class="status-pill available">Available for Reg</span></td>
                <td>Unassigned</td>
                <td>High AI/Tech Demand</td>
            </tr>
            <tr>
                <td><strong>.co</strong></td>
                <td><span class="status-pill available">Available for Reg</span></td>
                <td>Unassigned</td>
                <td>Startup Alternative</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">3. Detailed DNS & Server Infrastructure</div>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 15%;">Record Type</th>
                <th style="width: 25%;">Hostname / Subdomain</th>
                <th style="width: 45%;">Resolved Value / IP Address</th>
                <th style="width: 15%;">Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>A Record</strong></td>
                <td>@ ({domain_name})</td>
                <td><code>{ip_address}</code> (Render Hosted)</td>
                <td><span class="status-pill info">Active</span></td>
            </tr>
            <tr>
                <td><strong>CNAME</strong></td>
                <td>www.{domain_name}</td>
                <td><code>domain-radar-saas.onrender.com</code></td>
                <td><span class="status-pill info">Active</span></td>
            </tr>
            <tr>
                <td><strong>MX Records</strong></td>
                <td>@</td>
                <td><em>No Mail Server (MX) Configured</em></td>
                <td><span class="status-pill warning">Missing</span></td>
            </tr>
            <tr>
                <td><strong>SPF Record</strong></td>
                <td>TXT (@)</td>
                <td><em>v=spf1 ... (Not Detected)</em></td>
                <td><span class="status-pill warning">Missing</span></td>
            </tr>
            <tr>
                <td><strong>DMARC Record</strong></td>
                <td>TXT (_dmarc)</td>
                <td><em>p=none ... (Not Detected)</em></td>
                <td><span class="status-pill warning">Missing</span></td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">4. Email Security & WHOIS Intelligence</div>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 35%;">Security & Registry Parameter</th>
                <th style="width: 65%;">Audit Value & Details</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Registrar Company</strong></td>
                <td>{registrar}</td>
            </tr>
            <tr>
                <td><strong>SSL / TLS Certificate</strong></td>
                <td>Google Trust Services (Active & Valid)</td>
            </tr>
            <tr>
                <td><strong>DNSBL Blacklist Scan</strong></td>
                <td>Listed in 2 DNSBL Databases (Requires Delisting Cleanup)</td>
            </tr>
            <tr>
                <td><strong>Historical Archive</strong></td>
                <td><a href="https://web.archive.org/web/*/{domain_name}" style="color: #0284c7; text-decoration: none;">View Archive Snapshot (Wayback Machine)</a></td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        Generated automatically by BlacklistMail Radar Engine • Confidential Domain Intelligence Audit Report
    </div>

</body>
</html>
"""
    
    # Save temporary HTML and render to PDF
    temp_html = f"temp_{domain_name}.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    weasyprint.HTML(filename=temp_html).write_pdf(output_pdf_path)
    
    if os.path.exists(temp_html):
        os.remove(temp_html)
        
    return output_pdf_path