# routers/services.py
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from utils import build_head_tags, MONETIZATION_HTML

router = APIRouter()

# 1. Platform / Overview
@router.get("/platform", response_class=HTMLResponse)
async def platform_page():
    head = build_head_tags(
        title="Email Security & Deliverability Platform | BlacklistMail",
        description="Comprehensive email security, blacklist monitoring, and DNS configuration suite.",
        canonical_url="https://blacklistmail.com/platform"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Home</a></p>
    <h1>🚀 BlacklistMail Platform</h1><p>All-in-one suite for monitoring domain reputation, deliverability, and DNS security.</p>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)

# 2. Delisting Directory
# routers/services.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from utils import build_head_tags

router = APIRouter(tags=["Services"])

@router.get("/delisting-directory", response_class=HTMLResponse)
async def delisting_directory():
    head = build_head_tags(
        title="Blacklist Delisting Directory | BlacklistMail",
        description="Official removal request links for major email blacklists.",
        canonical_url="https://blacklistmail.com/delisting-directory"
    )
    
    html = f'''<!DOCTYPE html>
    <html lang="en">
    {head}
    <style>
        :root {{
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --border-color: #30363d;
            --accent-blue: #2f81f7;
            --text-main: #c9d1d9;
            --text-heading: #f0f6fc;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0; padding: 0; line-height: 1.6;
        }}
        .navbar {{ background: #161b22; border-bottom: 1px solid var(--border-color); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .navbar a {{ color: var(--accent-blue); text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 1000px; margin: 50px auto; padding: 0 20px; }}
        .header {{ margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.2rem; color: var(--text-heading); margin-bottom: 10px; }}
        .header p {{ color: #8b949e; font-size: 1.1rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 25px; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-3px); border-color: var(--accent-blue); }}
        .card h3 {{ color: var(--text-heading); margin: 0 0 10px 0; font-size: 1.25rem; }}
        .card p {{ color: #8b949e; font-size: 0.92rem; margin-bottom: 20px; flex-grow: 1; }}
        .btn {{ display: inline-block; text-align: center; background: #21262d; color: var(--accent-blue); border: 1px solid var(--border-color); padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; }}
        .btn:hover {{ background: var(--accent-blue); color: #ffffff; }}
    </style>
    <body>
        <div class="navbar">
            <strong>BlacklistMail Directory</strong>
            <a href="/">&larr; Back to Home</a>
        </div>
        <div class="container">
            <div class="header">
                <h1>📋 Blacklist Delisting Directory</h1>
                <p>Direct removal application portals for major domain and IP DNSBL databases.</p>
            </div>
            <div class="grid">
                <div class="card">
                    <div>
                        <h3>Spamhaus Removal</h3>
                        <p>Global leader in IP/Domain threat reputation. Submit delist requests for SBL, DBL, and ZEN.</p>
                    </div>
                    <a href="https://check.spamhaus.org/" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
                <div class="card">
                    <div>
                        <h3>Barracuda Central</h3>
                        <p>Leading enterprise anti-spam firewall list. Request immediate IP reputation re-evaluation.</p>
                    </div>
                    <a href="https://www.barracudacentral.org/lookups" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
                <div class="card">
                    <div>
                        <h3>SpamCop Database</h3>
                        <p>Automated reporting database tracking IP addresses flagged for unsolicited bulk emails.</p>
                    </div>
                    <a href="https://www.spamcop.net/bl.shtml" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
                <div class="card">
                    <div>
                        <h3>Proofpoint (SORBS)</h3>
                        <p>Database indexing open relays and proxy servers causing email deliverability issues.</p>
                    </div>
                    <a href="http://www.sorbs.net/lookup.shtml" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
            </div>
        </div>
    </body>
    </html>'''
    return HTMLResponse(content=html)
# 4. Security News
@router.get("/news", response_class=HTMLResponse)
async def security_news():
    head = build_head_tags(
        title="Email Security News & Deliverability Trends | BlacklistMail",
        description="Stay updated with the latest trends in email authentication, SPF/DMARC policies, and inbox placement.",
        canonical_url="https://blacklistmail.com/news"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Home</a></p>
    <h1>📰 Security News & Insights</h1>
    <p>Insights on email authentication protocols, blacklist updates, and domain reputation management.</p>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)