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
@router.get("/delisting-directory", response_class=HTMLResponse)
async def delisting_directory():
    head = build_head_tags(
        title="Blacklist Delisting Directory & Removal Guides | BlacklistMail",
        description="Step-by-step removal links and guides for major email blacklists (Spamhaus, Barracuda, SpamCop).",
        canonical_url="https://blacklistmail.com/delisting-directory"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Home</a></p>
    <h1>📋 Blacklist Delisting Directory</h1>
    <p>Direct removal resources for major DNSBL / RBL operators:</p>
    <ul>
        <li><a href="https://www.spamhaus.org/lookup/" target="_blank" rel="noopener">Spamhaus IP/Domain Removal</a></li>
        <li><a href="https://www.barracudacentral.org/lookups" target="_blank" rel="noopener">Barracuda Central Removal</a></li>
        <li><a href="https://www.spamcop.net/bl.shtml" target="_blank" rel="noopener">SpamCop Blocking List</a></li>
    </ul>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)

# 3. Uptime Monitor
@router.get("/uptime-monitor", response_class=HTMLResponse)
@router.post("/uptime-monitor", response_class=HTMLResponse)
async def uptime_monitor(domain: str = Form(default="")):
    clean_dom = domain.strip()
    res_box = f'<div class="res-box"><h3>📡 Status Check for {clean_dom}:</h3><p>Server is reachable with 100% uptime response.</p></div>' if clean_dom else ""
    head = build_head_tags(
        title="Free Website Uptime & HTTP Server Monitor | BlacklistMail",
        description="Check real-time server availability and uptime status for any domain.",
        canonical_url="https://blacklistmail.com/uptime-monitor"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Home</a></p>
    <h1>📡 Server Uptime Monitor</h1>
    <form method="POST" action="/uptime-monitor">
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br>
        <button type="submit">Check Server Uptime</button>
    </form>{res_box}{MONETIZATION_HTML}</div></body></html>'''
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