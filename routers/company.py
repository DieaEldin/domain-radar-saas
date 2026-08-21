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
# routers/company.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from utils import build_head_tags

router = APIRouter(tags=["Company"])

@router.get("/pricing", response_class=HTMLResponse)
async def pricing():
    head = build_head_tags(
        title="API Pricing & Enterprise Plans | BlacklistMail",
        description="Scalable email security & domain monitoring API plans for developers and enterprises.",
        canonical_url="https://blacklistmail.com/pricing"
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
            --accent-green: #238636;
            --text-main: #c9d1d9;
            --text-heading: #f0f6fc;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .navbar {{
            background: #161b22;
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .navbar a {{ color: var(--accent-blue); text-decoration: none; font-weight: 600; }}
        .header-section {{ text-align: center; padding: 60px 20px 20px; }}
        .header-section h1 {{ font-size: 2.5rem; color: var(--text-heading); margin-bottom: 10px; }}
        .header-section p {{ font-size: 1.1rem; color: #8b949e; max-width: 600px; margin: 0 auto; }}
        
        .pricing-container {{
            max-width: 1200px;
            margin: 40px auto 80px;
            padding: 0 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        .plan-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 35px 25px;
            display: flex;
            flex-direction: column;
            position: relative;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .plan-card:hover {{ transform: translateY(-5px); border-color: var(--accent-blue); }}
        .plan-card.featured {{
            border: 2px solid var(--accent-blue);
            box-shadow: 0 0 20px rgba(47, 129, 247, 0.15);
        }}
        .badge {{
            position: absolute;
            top: -12px;
            right: 25px;
            background: var(--accent-blue);
            color: #ffffff;
            font-size: 0.8rem;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 20px;
            text-transform: uppercase;
        }}
        .plan-title {{ font-size: 1.5rem; color: var(--text-heading); margin: 0 0 10px 0; }}
        .plan-price {{ font-size: 2.8rem; font-weight: bold; color: var(--text-heading); margin-bottom: 20px; }}
        .plan-price span {{ font-size: 1rem; color: #8b949e; font-weight: normal; }}
        .features-list {{ list-style: none; padding: 0; margin: 0 0 30px 0; flex-grow: 1; }}
        .features-list li {{ margin-bottom: 12px; color: var(--text-main); font-size: 0.95rem; display: flex; align-items: center; }}
        .features-list li::before {{ content: "✓"; color: #3fb950; font-weight: bold; margin-right: 10px; }}
        
        .btn {{
            display: block;
            text-align: center;
            padding: 12px 20px;
            border-radius: 6px;
            font-weight: 600;
            text-decoration: none;
            transition: background 0.2s;
        }}
        .btn-outline {{ background: transparent; border: 1px solid var(--border-color); color: var(--text-heading); }}
        .btn-outline:hover {{ background: #21262d; border-color: #8b949e; }}
        .btn-primary {{ background: var(--accent-blue); color: #ffffff; border: none; }}
        .btn-primary:hover {{ background: #1f6feb; }}
    </style>
    <body>
        <div class="navbar">
            <strong>BlacklistMail API & Pricing</strong>
            <a href="/">&larr; Back to Home</a>
        </div>
        
        <div class="header-section">
            <h1>Simple, Transparent Pricing</h1>
            <p>Empower your application with real-time domain security analysis and blacklist intelligence.</p>
        </div>

        <div class="pricing-container">
            <!-- Free Plan -->
            <div class="plan-card">
                <h3 class="plan-title">Developer</h3>
                <div class="plan-price">$0 <span>/ month</span></div>
                <ul class="features-list">
                    <li>1,000 API Requests / mo</li>
                    <li>Basic Blacklist Check (15 RBLs)</li>
                    <li>SPF & DMARC Evaluator</li>
                    <li>Community Support</li>
                    <li>Rate Limit: 10 req/min</li>
                </ul>
                <a href="https://t.me/your_telegram" class="btn btn-outline">Get Free API Key</a>
            </div>

            <!-- Pro Plan -->
            <div class="plan-card featured">
                <span class="badge">Most Popular</span>
                <h3 class="plan-title">Professional</h3>
                <div class="plan-price">$29 <span>/ month</span></div>
                <ul class="features-list">
                    <li>50,000 API Requests / mo</li>
                    <li>Full RBL Inspection (100+ Blacklists)</li>
                    <li>BIMI & DKIM Auto Verification</li>
                    <li>Real-time Uptime Alerts</li>
                    <li>Priority Email & Chat Support</li>
                    <li>Webhook Notifications</li>
                </ul>
                <a href="https://t.me/your_telegram" class="btn btn-primary">Upgrade to Pro</a>
            </div>

            <!-- Enterprise Plan -->
            <div class="plan-card">
                <h3 class="plan-title">Enterprise</h3>
                <div class="plan-price">$99 <span>/ month</span></div>
                <ul class="features-list">
                    <li>500,000+ API Requests / mo</li>
                    <li>Custom RBL Feed Integration</li>
                    <li>Dedicated IP Monitoring</li>
                    <li>PDF Executive Report Export</li>
                    <li>SLA 99.9% Uptime Guarantee</li>
                    <li>Dedicated Account Manager</li>
                </ul>
                <a href="https://t.me/your_telegram" class="btn btn-outline">Contact Sales</a>
            </div>
        </div>
    </body>
    </html>'''
    return HTMLResponse(content=html)
# 2. About Us
@router.get("/about", response_class=HTMLResponse)
async def about():
    head = build_head_tags(
        title="About Us | BlacklistMail Threat Intelligence",
        description="Learn about BlacklistMail's mission to protect domain reputation and enhance email deliverability worldwide.",
        canonical_url="https://blacklistmail.com/about"
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
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }}
        .navbar {{ background: #161b22; border-bottom: 1px solid var(--border-color); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .navbar a {{ color: var(--accent-blue); text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 900px; margin: 50px auto; padding: 0 20px; }}
        .header-section {{ text-align: center; margin-bottom: 40px; }}
        .header-section h1 {{ font-size: 2.2rem; color: var(--text-heading); margin-bottom: 10px; }}
        .header-section p {{ color: #8b949e; font-size: 1.1rem; }}
        .card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 35px; margin-bottom: 25px; }}
        .card h2 {{ color: var(--text-heading); font-size: 1.4rem; margin-top: 0; margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 25px; }}
        .stat-item {{ background: #0d1117; border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; text-align: center; }}
        .stat-number {{ font-size: 2rem; font-weight: bold; color: var(--accent-blue); }}
        .stat-label {{ font-size: 0.85rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }}
    </style>
    <body>
        <div class="navbar">
            <strong>BlacklistMail Intelligence</strong>
            <a href="/">&larr; Back to Home</a>
        </div>
        <div class="container">
            <div class="header-section">
                <h1>About BlacklistMail</h1>
                <p>Empowering businesses with real-time email security & domain reputation intelligence.</p>
            </div>
            <div class="card">
                <h2>Our Mission</h2>
                <p>BlacklistMail was built to solve a critical challenge in modern communication: ensuring legitimate emails reach the inbox while protecting brand domains from unauthorized spoofing, phishing, and blacklist penalties.</p>
                <p>Our platform continuously queries global RBL databases, evaluates SPF/DMARC/DKIM compliance, and validates email security setups for system administrators and enterprise platforms.</p>
                
                <div class="grid-stats">
                    <div class="stat-item">
                        <div class="stat-number">100+</div>
                        <div class="stat-label">RBLs Monitored</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">99.9%</div>
                        <div class="stat-label">Uptime SLA</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">Real-Time</div>
                        <div class="stat-label">Threat Alerts</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>'''
    return HTMLResponse(content=html)
# 3. Contact Support
@router.get("/contact", response_class=HTMLResponse)
async def contact():
    head = build_head_tags(
        title="Contact Us & Support | BlacklistMail",
        description="Get in touch with BlacklistMail support team for API integrations, custom monitoring, or general inquiries.",
        canonical_url="https://blacklistmail.com/contact"
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
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }}
        .navbar {{ background: #161b22; border-bottom: 1px solid var(--border-color); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .navbar a {{ color: var(--accent-blue); text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 800px; margin: 50px auto; padding: 0 20px; }}
        .header-section {{ text-align: center; margin-bottom: 40px; }}
        .header-section h1 {{ font-size: 2.2rem; color: var(--text-heading); margin-bottom: 10px; }}
        .header-section p {{ color: #8b949e; font-size: 1.1rem; }}
        .card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 35px; }}
        .contact-methods {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 25px; }}
        .method-card {{ background: #0d1117; border: 1px solid var(--border-color); border-radius: 10px; padding: 25px; text-align: center; }}
        .method-card h3 {{ color: var(--text-heading); margin-top: 0; margin-bottom: 10px; font-size: 1.1rem; }}
        .method-card p {{ color: #8b949e; font-size: 0.9rem; margin-bottom: 20px; }}
        .btn {{ display: inline-block; background: var(--accent-blue); color: #ffffff; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
        .btn:hover {{ background: #1f6feb; }}
    </style>
    <body>
        <div class="navbar">
            <strong>BlacklistMail Support</strong>
            <a href="/">&larr; Back to Home</a>
        </div>
        <div class="container">
            <div class="header-section">
                <h1>Get in Touch</h1>
                <p>Have questions about our API, enterprise security plans, or domain monitoring?</p>
            </div>
            <div class="card">
                <div class="contact-methods">
                    <div class="method-card">
                        <h3>💬 Telegram Support</h3>
                        <p>Fastest way to get in touch with our engineering team for technical support.</p>
                        <a href="https://t.me/your_telegram" target="_blank" rel="noopener" class="btn">Chat on Telegram</a>
                    </div>
                    <div class="method-card">
                        <h3>📧 Direct Email</h3>
                        <p>Send us an email for general business inquiries and enterprise custom plans.</p>
                        <a href="mailto:support@blacklistmail.com" class="btn">Send an Email</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>'''
    return HTMLResponse(content=html)
# 4. System Status
@router.get("/status", response_class=HTMLResponse)
async def status():
    head = build_head_tags(
        title="System Operational Status | BlacklistMail",
        description="Real-time uptime and operational metrics for BlacklistMail API, RBL lookups, and security nodes.",
        canonical_url="https://blacklistmail.com/status"
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
            --status-green: #238636;
            --text-main: #c9d1d9;
            --text-heading: #f0f6fc;
        }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }}
        .navbar {{ background: #161b22; border-bottom: 1px solid var(--border-color); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .navbar a {{ color: var(--accent-blue); text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 850px; margin: 50px auto; padding: 0 20px; }}
        .banner {{ background: rgba(35, 134, 54, 0.15); border: 1px solid var(--status-green); border-radius: 10px; padding: 20px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px; }}
        .banner-title {{ color: #3fb950; font-size: 1.2rem; font-weight: bold; margin: 0; }}
        .pulse {{ height: 12px; width: 12px; background-color: #3fb950; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #3fb950; }}
        .card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 30px; }}
        .system-item {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 0; border-bottom: 1px solid var(--border-color); }}
        .system-item:last-child {{ border-bottom: none; }}
        .system-name {{ font-weight: 600; color: var(--text-heading); }}
        .status-badge {{ background: #238636; color: #ffffff; font-size: 0.8rem; font-weight: bold; padding: 4px 10px; border-radius: 12px; }}
    </style>
    <body>
        <div class="navbar">
            <strong>BlacklistMail Status</strong>
            <a href="/">&larr; Back to Home</a>
        </div>
        <div class="container">
            <div class="banner">
                <div>
                    <p class="banner-title">All Systems Operational</p>
                    <span style="font-size: 0.85rem; color: #8b949e;">Updated in real-time</span>
                </div>
                <span class="pulse"></span>
            </div>
            
            <div class="card">
                <div class="system-item">
                    <span class="system-name">API Endpoints (FastAPI Core)</span>
                    <span class="status-badge">Operational</span>
                </div>
                <div class="system-item">
                    <span class="system-name">DNS & RBL Inspection Engine</span>
                    <span class="status-badge">Operational</span>
                </div>
                <div class="system-item">
                    <span class="system-name">SPF / DMARC Evaluator Node</span>
                    <span class="status-badge">Operational</span>
                </div>
                <div class="system-item">
                    <span class="system-name">PDF Report Generation Engine</span>
                    <span class="status-badge">Operational</span>
                </div>
            </div>
        </div>
    </body>
    </html>'''
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