from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from engines.strategy_engine import generate_strategy
from engines.content_generator import generate_content
from engines.variation_engine import generate_variations
from engines.platform_adapter import adapt_platform

from core.memory import save_memory, get_memory
from engines.smart_post_engine import decide_post_plan
from engines.growth_engine import decide_growth_strategy
from engines.publish_engine import generate_publish_links
from engines.brain_engine import analyze_and_decide
from engines.feedback_engine import analyze_feedback
from engines.prompt_brain import understand_prompt
from engines.campaign_engine import generate_campaign
from engines.distribution_engine import create_distribution_plan
from engines.conversion_engine import generate_conversion_assets
from engines.visual_engine import generate_visual_assets
from engines.competitor_engine import analyze_market
from engines.publishing_engine import build_publish_queue
from engines.mastermind_engine import build_mastermind
from engines.autopilot_content_engine import generate_autopilot_content
from engines.orchestrator_engine import orchestrate
from engines.trend_radar_engine import scan_trends
from engines.analytics_engine import generate_dashboard_stats

app = FastAPI()


# ── HOME ──────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DropMeOnline</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:'Inter',sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);padding:20px}
        body::before,body::after{content:'';position:fixed;border-radius:50%;filter:blur(80px);opacity:.25;pointer-events:none}
        body::before{width:400px;height:400px;background:#7c3aed;top:-100px;left:-100px}
        body::after{width:350px;height:350px;background:#2563eb;bottom:-80px;right:-80px}
        .card{background:rgba(255,255,255,.07);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.12);border-radius:24px;padding:48px 40px;width:100%;max-width:480px;box-shadow:0 25px 50px rgba(0,0,0,.4)}
        .badge{display:inline-block;background:rgba(124,58,237,.3);border:1px solid rgba(124,58,237,.5);color:#c4b5fd;font-size:11px;font-weight:500;letter-spacing:1.5px;text-transform:uppercase;padding:4px 12px;border-radius:20px;margin-bottom:20px}
        h1{font-size:28px;font-weight:600;color:#fff;margin-bottom:8px;line-height:1.3}
        .subtitle{font-size:14px;color:rgba(255,255,255,.45);margin-bottom:36px;line-height:1.6}
        label{display:block;font-size:12px;font-weight:500;color:rgba(255,255,255,.5);letter-spacing:.8px;text-transform:uppercase;margin-bottom:10px}
        input[type=text]{width:100%;padding:14px 18px;font-size:14px;font-family:'Inter',sans-serif;color:#fff;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:12px;outline:none;transition:border-color .2s;margin-bottom:20px}
        input[type=text]::placeholder{color:rgba(255,255,255,.25)}
        input[type=text]:focus{border-color:rgba(124,58,237,.6);background:rgba(255,255,255,.09)}
        button{width:100%;padding:14px;font-size:14px;font-weight:600;font-family:'Inter',sans-serif;color:#fff;background:linear-gradient(135deg,#7c3aed,#2563eb);border:none;border-radius:12px;cursor:pointer;letter-spacing:.3px;transition:opacity .2s,transform .1s}
        button:hover{opacity:.88;transform:translateY(-1px)}
        .divider{height:1px;background:rgba(255,255,255,.08);margin:28px 0}
        .memory-link{text-align:center;font-size:13px;color:rgba(255,255,255,.35)}
        .memory-link a{color:#a78bfa;text-decoration:none;font-weight:500}
        .memory-link a:hover{color:#c4b5fd}
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">AI Strategist</div>
        <h1>DropMeOnline</h1>
        <p class="subtitle">Your personal AI-powered social media strategist. Enter a goal and let the engine do the rest.</p>
        <form action="/generate-strategy" method="post">
            <label for="goal">Your Goal</label>
            <input type="text" id="goal" name="goal" placeholder="e.g. Grow AI niche for 30 days" required />
            <button type="submit">Generate Strategy →</button>
        </form>
        <div class="divider"></div>
        <div class="memory-link">View past strategies → <a href="/memory">Memory</a></div>
    </div>
</body>
</html>"""


# ── GENERATE STRATEGY ─────────────────────────────────────────────────────────
@app.post("/generate-strategy", response_class=HTMLResponse)
def generate(goal: str = Form(...)):

    # ── Run all engines ──
    result       = generate_strategy(goal)
    prompt_data  = understand_prompt(goal)
    mind         = build_mastermind(goal, prompt_data)
    flow         = orchestrate(goal, prompt_data)

    primary_platform = prompt_data["platforms"][0] if prompt_data["platforms"] else "linkedin"
    active_platforms = prompt_data["platforms"] if prompt_data["platforms"] else ["linkedin"]

    trends  = scan_trends(goal, result["niche"], prompt_data["audience"], primary_platform)
    stats   = generate_dashboard_stats()
    save_memory(result)

    content      = generate_content(goal)
    auto_content = generate_autopilot_content(goal, primary_platform, result["niche"], prompt_data["audience"], [], mind)
    plan         = decide_post_plan(goal)
    growth       = decide_growth_strategy(goal, "linkedin", {"engagement": "high", "last_posts": 5})
    brain        = analyze_and_decide("linkedin", {"reach": 1200, "likes": 85, "comments": 14, "post_time": "09:00", "frequency": "daily"})
    feedback_result = analyze_feedback("linkedin", {"reach": "medium", "likes": "high", "comments": "medium", "time": "morning", "overall": "good"})
    adapted      = adapt_platform(content)
    links        = generate_publish_links(content)
    variations   = generate_variations(goal)
    campaign     = generate_campaign(goal, 30, active_platforms)
    distribution = create_distribution_plan(30, active_platforms, 2)
    conversion   = generate_conversion_assets(goal)
    visuals      = generate_visual_assets(goal, auto_content, mind, primary_platform)
    market       = analyze_market(goal)
    publish      = build_publish_queue(campaign, active_platforms)

    # ── Safe string helpers ──
    def li(items, limit=4):
        return "".join(f"<li>{x}</li>" for x in items[:limit])

    def safe(val):
        return str(val).replace("{", "").replace("}", "")

    # ── Build calendar rows ──
    cal_rows = ""
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, item in enumerate(campaign[:7]):
        day_label = days_of_week[i % 7]
        cal_rows += f"""
        <div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
            <div style="min-width:36px;font-family:sans-serif;font-size:15px;font-weight:700;color:#7c3aed;">{item['day']}</div>
            <div>
                <div style="font-size:10px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:1px;">{day_label}</div>
                <div style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:2px;">{safe(item['theme'])} — {safe(item['hook'])[:55]}...</div>
            </div>
        </div>"""

    # ── Platform content helpers ──
    li_post_1  = safe(auto_content["post"])
    li_post_2  = safe(adapted.get("linkedin", ""))
    ig_post_1  = safe(adapted.get("instagram", ""))
    ig_post_2  = safe(content.get("instagram", ""))
    tw_tweet_1 = safe(adapted.get("twitter", ""))
    tw_tweet_2 = safe(auto_content["hook"])
    tw_tweet_3 = safe(auto_content["cta"])

    li_carousel = safe(visuals.get("headline", ""))
    ig_reel     = f"Reel concept: {safe(visuals.get('image_prompt', ''))[:120]}..."
    ig_story    = f"Story idea: {safe(auto_content.get('image_idea', ''))[:120]}..."
    tw_thread   = safe(mind["top_hooks"][0]) if mind.get("top_hooks") else safe(auto_content["hook"])

    li_url = links.get("linkedin_url", "#")
    tw_url = links.get("twitter_url", "#")

    # ── Render HTML ──
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DropMeOnline — Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
        body{min-height:100vh;font-family:'Inter',sans-serif;background:#07050f;color:#e2e8f0;padding:0 0 80px}
        .orb{position:fixed;border-radius:50%;filter:blur(120px);pointer-events:none;z-index:0}
        .orb-1{width:600px;height:600px;background:#4c1d95;opacity:.12;top:-200px;left:-200px}
        .orb-2{width:500px;height:500px;background:#1e3a8a;opacity:.10;bottom:-150px;right:-150px}
        .page{position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:0 20px}
        /* Header */
        .header{padding:28px 0 24px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,.06);margin-bottom:32px}
        .logo{font-family:'Syne',sans-serif;font-size:20px;font-weight:800;background:linear-gradient(135deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
        .goal-pill{font-size:12px;color:rgba(255,255,255,.35);max-width:360px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-left:12px}
        .badge-active{display:inline-flex;align-items:center;gap:7px;background:rgba(134,239,172,.08);border:1px solid rgba(134,239,172,.2);color:#86efac;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:6px 14px;border-radius:20px}
        .pulse{width:7px;height:7px;background:#86efac;border-radius:50%;animation:pulse 2s infinite}
        @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.8)}}
        /* Cards */
        .card{background:rgba(255,255,255,.04);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:26px;transition:border-color .3s}
        .card:hover{border-color:rgba(124,58,237,.25)}
        .section-label{font-size:10px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#7c3aed;margin-bottom:16px}
        /* Action grid */
        .action-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
        .astat{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:18px;transition:all .25s}
        .astat:hover{background:rgba(124,58,237,.07);border-color:rgba(124,58,237,.25)}
        .astat .lbl{font-size:10px;font-weight:600;color:rgba(255,255,255,.28);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px}
        .astat .val{font-size:14px;font-weight:600;color:#e2e8f0}
        .val-purple{color:#a78bfa!important}
        .val-green{color:#86efac!important}
        .val-blue{color:#93c5fd!important}
        /* Tabs */
        .tab-bar{display:flex;gap:4px;margin-bottom:18px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:5px}
        .tab{flex:1;padding:10px 14px;font-size:12px;font-weight:600;font-family:'Inter',sans-serif;color:rgba(255,255,255,.3);background:none;border:none;border-radius:10px;cursor:pointer;transition:all .2s;text-align:center}
        .tab:hover{color:rgba(255,255,255,.65);background:rgba(255,255,255,.04)}
        .tab.active{color:#fff;background:linear-gradient(135deg,rgba(109,40,217,.5),rgba(37,99,235,.4));border:1px solid rgba(167,139,250,.2)}
        .tab-panel{display:none}
        .tab-panel.active{display:block}
        /* Post items */
        .pitem{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:18px;margin-bottom:10px;position:relative;overflow:hidden;transition:all .25s}
        .pitem::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:linear-gradient(180deg,#7c3aed,#2563eb);opacity:0;transition:opacity .25s}
        .pitem:hover{border-color:rgba(124,58,237,.2);background:rgba(124,58,237,.04)}
        .pitem:hover::before{opacity:1}
        .ptag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:3px 10px;border-radius:20px;margin-bottom:10px}
        .tag-li{background:rgba(37,99,235,.12);border:1px solid rgba(37,99,235,.25);color:#93c5fd}
        .tag-ig{background:rgba(236,72,153,.1);border:1px solid rgba(236,72,153,.25);color:#f9a8d4}
        .tag-tw{background:rgba(14,165,233,.1);border:1px solid rgba(14,165,233,.25);color:#7dd3fc}
        .tag-idea{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);color:#fcd34d}
        .pcontent{font-size:13px;color:rgba(255,255,255,.6);line-height:1.75;white-space:pre-line}
        .prow{display:flex;align-items:center;justify-content:space-between;margin-top:12px}
        .copy-btn{font-size:11px;font-weight:600;font-family:'Inter',sans-serif;color:rgba(255,255,255,.35);background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:8px;padding:5px 12px;cursor:pointer;transition:all .2s}
        .copy-btn:hover{color:#fff;background:rgba(124,58,237,.18);border-color:rgba(124,58,237,.35)}
        /* Layout */
        .main-grid{display:grid;grid-template-columns:1fr 310px;gap:20px;align-items:start}
        .left-col,.right-col{display:flex;flex-direction:column;gap:18px}
        /* Visual card */
        .vgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
        .vstat{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:13px;padding:14px 16px}
        .vfull{grid-column:span 2}
        .vlbl{font-size:10px;font-weight:600;color:rgba(255,255,255,.26);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px}
        .vval{font-size:13px;color:#c4b5fd;line-height:1.6}
        /* Publish buttons */
        .pub-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
        .pub-btn{display:block;text-align:center;padding:13px;font-size:12px;font-weight:600;font-family:'Inter',sans-serif;border-radius:12px;text-decoration:none;cursor:pointer;transition:all .2s;border:none}
        .pub-li{color:#93c5fd;background:rgba(37,99,235,.1);border:1px solid rgba(37,99,235,.25)}
        .pub-li:hover{background:rgba(37,99,235,.22);transform:translateY(-2px)}
        .pub-ig{color:#f9a8d4;background:rgba(236,72,153,.08);border:1px solid rgba(236,72,153,.2)}
        .pub-ig:hover{background:rgba(236,72,153,.18);transform:translateY(-2px)}
        .pub-tw{color:#7dd3fc;background:rgba(14,165,233,.08);border:1px solid rgba(14,165,233,.2)}
        .pub-tw:hover{background:rgba(14,165,233,.18);transform:translateY(-2px)}
        /* Analytics row */
        .stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
        .sstat{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:16px}
        .sstat .lbl{font-size:10px;font-weight:600;color:rgba(255,255,255,.26);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:7px}
        .sstat .val{font-size:22px;font-weight:700;font-family:'Syne',sans-serif;color:#a78bfa}
        /* Back */
        .back{display:inline-flex;align-items:center;gap:6px;color:rgba(255,255,255,.25);font-size:12px;text-decoration:none;transition:color .2s}
        .back:hover{color:#a78bfa}
        /* Responsive */
        @media(max-width:900px){.main-grid{grid-template-columns:1fr}.action-grid{grid-template-columns:1fr 1fr}.stats-row{grid-template-columns:1fr 1fr}.pub-row{grid-template-columns:1fr}}
        @media(max-width:480px){.action-grid{grid-template-columns:1fr}}
    </style>
</head>
<body>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="page">

<!-- HEADER -->
<div class="header">
    <div style="display:flex;align-items:center;">
        <span class="logo">DropMeOnline</span>
        <span class="goal-pill">""" + safe(goal) + """</span>
    </div>
    <div class="badge-active"><span class="pulse"></span>Autopilot Active</div>
</div>

<!-- ANALYTICS ROW -->
<div class="stats-row" style="margin-bottom:20px;">
    <div class="sstat"><div class="lbl">Posts Generated</div><div class="val">""" + str(stats["posts_generated"]) + """</div></div>
    <div class="sstat"><div class="lbl">Campaigns</div><div class="val">""" + str(stats["campaigns_created"]) + """</div></div>
    <div class="sstat"><div class="lbl">Growth Score</div><div class="val">""" + str(stats["growth_score"]) + """</div></div>
    <div class="sstat"><div class="lbl">Streak</div><div class="val">""" + str(stats.get("streak_days", 1)) + """d</div></div>
</div>

<!-- ACTION CENTER -->
<div class="card" style="margin-bottom:20px;">
    <div class="section-label">Today's Action Center</div>
    <div class="action-grid">
        <div class="astat"><div class="lbl">Best Platform</div><div class="val val-purple">""" + safe(stats["best_platform_today"]) + """</div></div>
        <div class="astat"><div class="lbl">Post Time</div><div class="val val-green">""" + safe(brain["next_post_time"]) + """</div></div>
        <div class="astat"><div class="lbl">Content Type</div><div class="val val-blue">""" + safe(growth["content_type"]) + """</div></div>
        <div class="astat"><div class="lbl">Next Action</div><div class="val" style="font-size:11px;color:rgba(255,255,255,.5);line-height:1.4;">""" + safe(stats["next_action"])[:80] + """...</div></div>
    </div>
</div>

<div class="main-grid">
<div class="left-col">

<!-- PLATFORM CONTENT TABS -->
<div class="card">
    <div class="section-label">Platform Content</div>
    <div class="tab-bar">
        <button class="tab active" onclick="switchTab('linkedin',this)">LinkedIn</button>
        <button class="tab" onclick="switchTab('instagram',this)">Instagram</button>
        <button class="tab" onclick="switchTab('twitter',this)">Twitter / X</button>
    </div>

    <!-- LinkedIn -->
    <div id="tab-linkedin" class="tab-panel active">
        <div class="pitem">
            <span class="ptag tag-li">Post 1 — Autopilot</span>
            <div class="pcontent">""" + li_post_1[:400] + """</div>
            <div class="prow">
                <span style="font-size:11px;color:rgba(255,255,255,.2);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + li_post_1.replace("'","").replace('"','')[:300] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-li">Post 2 — Adapted</span>
            <div class="pcontent">""" + li_post_2[:400] + """</div>
            <div class="prow">
                <span style="font-size:11px;color:rgba(255,255,255,.2);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + li_post_2.replace("'","").replace('"','')[:300] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-idea">Carousel Idea</span>
            <div class="pcontent">""" + li_carousel[:200] + """</div>
        </div>
    </div>

    <!-- Instagram -->
    <div id="tab-instagram" class="tab-panel">
        <div class="pitem">
            <span class="ptag tag-ig">Caption 1</span>
            <div class="pcontent">""" + ig_post_1[:400] + """</div>
            <div class="prow">
                <span style="font-size:11px;color:rgba(255,255,255,.2);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + ig_post_1.replace("'","").replace('"','')[:300] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-ig">Caption 2</span>
            <div class="pcontent">""" + ig_post_2[:400] + """</div>
            <div class="prow">
                <span style="font-size:11px;color:rgba(255,255,255,.2);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + ig_post_2.replace("'","").replace('"','')[:300] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem"><span class="ptag tag-idea">Reel Idea</span><div class="pcontent">""" + ig_reel[:200] + """</div></div>
        <div class="pitem"><span class="ptag tag-idea">Story Idea</span><div class="pcontent">""" + ig_story[:200] + """</div></div>
    </div>

    <!-- Twitter -->
    <div id="tab-twitter" class="tab-panel">
        <div class="pitem">
            <span class="ptag tag-tw">Tweet 1 — Bold Take</span>
            <div class="pcontent">""" + tw_tweet_1[:280] + """</div>
            <div class="prow">
                <span style="font-size:11px;color:rgba(255,255,255,.2);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + tw_tweet_1.replace("'","").replace('"','')[:250] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-tw">Tweet 2 — Hook</span>
            <div class="pcontent">""" + tw_tweet_2[:280] + """</div>
            <div class="prow">
                <span style="font-size:11px;color:rgba(255,255,255,.2);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + tw_tweet_2.replace("'","").replace('"','')[:250] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-tw">Tweet 3 — CTA</span>
            <div class="pcontent">""" + tw_tweet_3[:280] + """</div>
        </div>
        <div class="pitem"><span class="ptag tag-idea">Thread Hook</span><div class="pcontent">""" + safe(tw_thread)[:200] + """</div></div>
    </div>
</div>

<!-- PUBLISH -->
<div class="card">
    <div class="section-label">Publish Now</div>
    <div class="pub-row">
        <a href='""" + li_url + """' target="_blank" class="pub-btn pub-li">→ LinkedIn</a>
        <button class="pub-btn pub-ig" onclick="alert('Copy your Instagram caption above, then open the app.')">→ Instagram</button>
        <a href='""" + tw_url + """' target="_blank" class="pub-btn pub-tw">→ Twitter / X</a>
    </div>
</div>

<!-- STRATEGY INTEL -->
<div class="card">
    <div class="section-label">Strategy Intelligence</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
        <div class="vstat"><div class="vlbl">Niche</div><div class="vval" style="color:#e2e8f0;">""" + safe(result["niche"]) + """</div></div>
        <div class="vstat"><div class="vlbl">Trigger</div><div class="vval" style="color:#e2e8f0;">""" + safe(mind["psychology_trigger"]) + """</div></div>
        <div class="vstat"><div class="vlbl">Tone Lock</div><div class="vval" style="color:#e2e8f0;font-size:12px;">""" + safe(flow["tone_lock"])[:60] + """</div></div>
        <div class="vstat"><div class="vlbl">Frequency</div><div class="vval" style="color:#86efac;">""" + safe(plan["linkedin_frequency"]) + """</div></div>
    </div>
    <div style="margin-top:14px;padding:14px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:12px;font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;">
        """ + safe(flow["content_strategy"])[:300] + """
    </div>
</div>

</div><!-- end left-col -->

<!-- RIGHT COLUMN -->
<div class="right-col">

<!-- VISUAL STUDIO -->
<div class="card">
    <div class="section-label">Visual Studio</div>
    <div class="vgrid">
        <div class="vstat"><div class="vlbl">Format</div><div class="vval">""" + safe(visuals.get("format","")) + """</div></div>
        <div class="vstat"><div class="vlbl">Why It Works</div><div class="vval" style="font-size:11px;">""" + safe(visuals.get("why_it_works",""))[:80] + """</div></div>
        <div class="vstat vfull"><div class="vlbl">Headline</div><div class="vval">""" + safe(visuals.get("headline","")) + """</div></div>
        <div class="vstat vfull"><div class="vlbl">Image Prompt</div><div class="vval" style="font-size:11px;color:rgba(255,255,255,.4);">""" + safe(visuals.get("image_prompt",""))[:180] + """</div></div>
    </div>
</div>

<!-- 7 DAY CALENDAR -->
<div class="card">
    <div class="section-label">7-Day Calendar</div>
    """ + cal_rows + """
</div>

<!-- TREND RADAR -->
<div class="card">
    <div class="section-label">Trend Radar</div>
    <div style="font-size:12px;color:#a78bfa;font-weight:600;margin-bottom:8px;">Best topic today</div>
    <div style="font-size:13px;color:rgba(255,255,255,.65);line-height:1.6;margin-bottom:14px;">""" + safe(trends["best_topic_today"]) + """</div>
    <div style="font-size:11px;color:rgba(255,255,255,.3);margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;">Hot topics</div>
    <ul style="list-style:none;display:flex;flex-direction:column;gap:6px;">""" + "".join(f'<li style="font-size:12px;color:rgba(255,255,255,.5);padding:8px 10px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:8px;">{safe(x)[:90]}</li>' for x in trends["hot_topics"][:3]) + """</ul>
</div>

<!-- BACK -->
<a href="/" class="back" style="margin-top:4px;">← New Strategy</a>

</div><!-- end right-col -->
</div><!-- end main-grid -->
</div><!-- end page -->

<script>
function switchTab(n,btn){
    document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.getElementById('tab-'+n).classList.add('active');
    btn.classList.add('active');
}
function cp(btn,text){
    navigator.clipboard.writeText(text).then(()=>{
        btn.textContent='Copied!';btn.style.color='#86efac';
        setTimeout(()=>{btn.textContent='Copy';btn.style.color='';},2000);
    });
}
</script>
</body>
</html>"""

    return html


# ── FEEDBACK ──────────────────────────────────────────────────────────────────
@app.post("/update-feedback", response_class=HTMLResponse)
def update_feedback(
    reach: str = Form(...),
    likes: str = Form(...),
    comments: str = Form(...),
    overall: str = Form(...),
    platform: str = Form(...)
):
    result = analyze_feedback(platform, {
        "reach": reach, "likes": likes,
        "comments": comments, "time": "recent", "overall": overall
    })
    decision = result["decision"]
    badge_class = "badge-keep" if decision == "keep" else "badge-change"

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>AI Learning Updated</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{min-height:100vh;font-family:'Inter',sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#1a1a3e);display:flex;align-items:center;justify-content:center;padding:40px 20px}}
.wrap{{max-width:520px;width:100%}}
.banner{{background:linear-gradient(135deg,rgba(109,40,217,.3),rgba(37,99,235,.25));border:1px solid rgba(167,139,250,.2);border-radius:20px;padding:28px;text-align:center;margin-bottom:20px}}
.icon{{font-size:36px;display:block;margin-bottom:10px}}
.title{{font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#fff;margin-bottom:4px}}
.sub{{font-size:13px;color:rgba(255,255,255,.4)}}
.card{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:28px;margin-bottom:16px}}
.slabel{{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#7c3aed;margin-bottom:16px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.stat{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:14px 16px}}
.full{{grid-column:span 2}}
.lbl{{font-size:10px;color:rgba(255,255,255,.28);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px}}
.val{{font-size:14px;font-weight:500;color:#e2e8f0}}
.pill{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase}}
.badge-keep{{background:rgba(134,239,172,.1);border:1px solid rgba(134,239,172,.25);color:#86efac}}
.badge-change{{background:rgba(252,165,165,.1);border:1px solid rgba(252,165,165,.25);color:#fca5a5}}
.style-val{{font-size:13px;color:#c4b5fd;line-height:1.6}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px}}
.btn{{display:block;text-align:center;padding:13px;font-size:13px;font-weight:600;font-family:'Inter',sans-serif;border-radius:12px;text-decoration:none;transition:all .2s}}
.btn-p{{color:#fff;background:linear-gradient(135deg,#6d28d9,#2563eb)}}
.btn-p:hover{{opacity:.88;transform:translateY(-2px)}}
.btn-s{{color:rgba(255,255,255,.55);background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1)}}
.btn-s:hover{{color:#fff;background:rgba(255,255,255,.09)}}
.back{{display:inline-flex;color:rgba(255,255,255,.25);font-size:12px;text-decoration:none;margin-bottom:24px;transition:color .2s}}
.back:hover{{color:#a78bfa}}
</style></head><body>
<div class="wrap">
<a href="/" class="back">← Back</a>
<div class="banner"><span class="icon">🧠</span><div class="title">AI Learning Updated</div><div class="sub">Strategy adjusted based on your feedback</div></div>
<div class="card">
<div class="slabel">Updated Strategy</div>
<div class="grid">
<div class="stat"><div class="lbl">Platform</div><div class="val">{platform}</div></div>
<div class="stat"><div class="lbl">Decision</div><div class="val"><span class="pill {badge_class}">{result['decision'].upper()}</span></div></div>
<div class="stat"><div class="lbl">Next Post Time</div><div class="val">{result['next_time']}</div></div>
<div class="stat"><div class="lbl">Frequency</div><div class="val">{result['frequency']}</div></div>
<div class="stat full"><div class="lbl">Recommended Style</div><div class="style-val">{result['content_style']}</div></div>
</div>
</div>
<div class="row">
<a href="/" class="btn btn-s">← Home</a>
<a href="/" class="btn btn-p">New Strategy →</a>
</div>
</div></body></html>"""


# ── MEMORY ────────────────────────────────────────────────────────────────────
@app.get("/memory", response_class=HTMLResponse)
def view_memory():
    memory = get_memory()
    items = ""
    for item in memory:
        if isinstance(item, dict) and "goal" in item:
            items += f"<li style='padding:8px 0;border-bottom:1px solid rgba(255,255,255,.06);color:rgba(255,255,255,.6);font-size:13px;'>{item['goal']}</li>"
        else:
            items += f"<li style='padding:8px 0;color:rgba(255,255,255,.4);font-size:12px;'>{str(item)[:80]}</li>"

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Memory — DropMeOnline</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{min-height:100vh;font-family:'Inter',sans-serif;background:#07050f;color:#e2e8f0;display:flex;align-items:center;justify-content:center;padding:40px 20px}}.wrap{{max-width:520px;width:100%}}.title{{font-family:'Syne',sans-serif;font-size:22px;font-weight:700;color:#fff;margin-bottom:24px}}.card{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:24px}}ul{{list-style:none}}.back{{display:inline-block;color:rgba(255,255,255,.3);font-size:12px;text-decoration:none;margin-bottom:20px;transition:color .2s}}.back:hover{{color:#a78bfa}}</style>
</head><body><div class="wrap">
<a href="/" class="back">← Back</a>
<div class="title">Past Strategies</div>
<div class="card"><ul>{items if items else '<li style="color:rgba(255,255,255,.3);font-size:13px;">No strategies yet.</li>'}</ul></div>
</div></body></html>"""