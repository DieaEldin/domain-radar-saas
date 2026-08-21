# routers/company.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from utils import build_head_tags, MONETIZATION_HTML

router = APIRouter(tags=["Company & Static Pages"])

# تصميم CSS موحد وبسيط لضمان احترافية المظهر
COMMON_STYLE = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
    .navbar { background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
    .navbar a { color: #2563eb; text-decoration: none; font-weight: 600; }
    .container { max-width: 800px; margin: 40px auto; padding: 0 20px; }
    .card { background: #ffffff; padding: 35px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    h1 { color: #1e293b; margin-top: 0; font-size: 2rem; }
    p { line-height: 1.6; color: #475569; }
    ul { line-height: 1.8; color: #334155; }
    a { color: #2563eb; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .status-badge { background: #d1fae5; color: #065f46; padding: 6px 12px; border-radius: 20px; font-weight: 600; display: inline-block; }
</style>
"""

# 1. API & Pricing
@router.get("/api-pricing", response_class=HTMLResponse)
@router.get("/pricing", response_class=HTMLResponse)
async def pricing_page():
    head = build_head_tags(
        title="API Access & Subscription Pricing Plans | BlacklistMail",
        description="Scalable pricing plans for developer API access, automated blacklist monitoring, and DNS lookup tools.",
        canonical_url="https://blacklistmail.com/pricing"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    {COMMON_STYLE}
    <body>
        <div class="navbar"><strong>BlacklistMail</strong><a href="/">&larr; Back to Home</a></div>
        <div class="container">
            <div class="card">
                <h1>💳 API & Pricing Plans</h1>
                <p>Choose the right plan for automated DNS monitoring, bulk lookup API access, and domain reputation protection.</p>
                <ul>
                    <li><strong>Free Plan:</strong> Unlimited manual web lookups for SPF, DMARC, and DKIM.</li>
                    <li><strong>Developer API:</strong> High-speed REST endpoints for domain tools and deliverability metrics.</li>
                    <li><strong>Enterprise Monitor:</strong> 24/7 continuous domain blacklist tracking and instant alerts.</li>
                </ul>
            </div>
            {MONETIZATION_HTML}
        </div>
    </body></html>'''
    return HTMLResponse(content=html)

# 2. About Us
@router.get("/about", response_class=HTMLResponse)
async def about_page():
    head = build_head_tags(
        title="About Us - Domain Security & Deliverability Experts | BlacklistMail",
        description="Learn more about BlacklistMail's mission to protect email deliverability and domain reputation.",
        canonical_url="https://blacklistmail.com/about"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    {COMMON_STYLE}
    <body>
        <div class="navbar"><strong>BlacklistMail</strong><a href="/">&larr; Back to Home</a></div>
        <div class="container">
            <div class="card">
                <h1>ℹ️ About BlacklistMail</h1>
                <p>We provide automated domain intelligence, deliverability diagnostics, and real-time DNS monitoring tools designed to secure email channels and preserve sender reputation.</p>
                <p>Our platform helps system administrators, web developers, and marketers detect infrastructure misconfigurations, generate compliant DNS records, and maintain optimal deliverability.</p>
            </div>
            {MONETIZATION_HTML}
        </div>
    </body></html>'''
    return HTMLResponse(content=html)

# 3. Contact Support
@router.get("/contact", response_class=HTMLResponse)
async def contact_page():
    head = build_head_tags(
        title="Contact Support | BlacklistMail",
        description="Get in touch with our technical team for help with domain monitoring, delisting, or API access.",
        canonical_url="https://blacklistmail.com/contact"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    {COMMON_STYLE}
    <body>
        <div class="navbar"><strong>BlacklistMail</strong><a href="/">&larr; Back to Home</a></div>
        <div class="container">
            <div class="card">
                <h1>✉️ Contact Support</h1>
                <p>For technical assistance, domain monitoring inquiries, or API access limits, reach out to our team:</p>
                <p><strong>Email:</strong> support@blacklistmail.com</p>
                <p>We aim to respond to all technical queries within 24 business hours.</p>
            </div>
            {MONETIZATION_HTML}
        </div>
    </body></html>'''
    return HTMLResponse(content=html)

# 4. System Status
@router.get("/status", response_class=HTMLResponse)
async def system_status():
    head = build_head_tags(
        title="System Operational Status | BlacklistMail Radar",
        description="Live operational metrics and service status across all DNS inspection nodes.",
        canonical_url="https://blacklistmail.com/status"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    {COMMON_STYLE}
    <body>
        <div class="navbar"><strong>BlacklistMail Status</strong><a href="/">&larr; Back to Home</a></div>
        <div class="container">
            <div class="card">
                <h1>🟢 System Status</h1>
                <p><span class="status-badge">All Systems Operational</span></p>
                <p>All core infrastructure services, DNS resolvers, and API nodes are <strong>100% Operational</strong>.</p>
            </div>
            {MONETIZATION_HTML}
        </div>
    </body></html>'''
    return HTMLResponse(content=html)

# 5. Sitemap Info
@router.get("/sitemap-info", response_class=HTMLResponse)
async def sitemap_info():
    head = build_head_tags(
        title="HTML Sitemap & Navigation Directory | BlacklistMail",
        description="Complete list of all free email security tools, generators, lookups, and resources.",
        canonical_url="https://blacklistmail.com/sitemap-info"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    {COMMON_STYLE}
    <body>
        <div class="navbar"><strong>BlacklistMail Directory</strong><a href="/">&larr; Back to Home</a></div>
        <div class="container">
            <div class="card">
                <h1>🗺️ Site Navigation Directory</h1>
                <p>Access all available email authentication, deliverability, and lookup tools:</p>
                <ul>
                    <li><a href="/spf-generator">SPF Generator</a> | <a href="/spf-checker">SPF Checker</a></li>
                    <li><a href="/dmarc-generator">DMARC Generator</a> | <a href="/dmarc-checker">DMARC Checker</a></li>
                    <li><a href="/bimi-generator">BIMI Generator</a> | <a href="/bimi-inspector">BIMI Inspector</a></li>
                    <li><a href="/dkim-checker">DKIM Checker</a></li>
                    <li><a href="/mx-lookup">MX Lookup</a> | <a href="/ptr-lookup">PTR Lookup</a></li>
                    <li><a href="/ssl-checker">SSL Checker</a> | <a href="/spam-analyzer">Spam Analyzer</a></li>
                </ul>
            </div>
            {MONETIZATION_HTML}
        </div>
    </body></html>'''
    return HTMLResponse(content=html)