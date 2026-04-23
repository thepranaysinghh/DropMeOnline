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
from engines.image_engine import generate_images

app = FastAPI()

# ── SHARED DESIGN SYSTEM ──────────────────────────────────────────────────────
# One CSS variable sheet + shared styles injected into every page
DESIGN_SYSTEM = """
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
    --bg:        #0d0b1a;
    --surface:   rgba(255,255,255,0.07);
    --surface2:  rgba(255,255,255,0.11);
    --border:    rgba(255,255,255,0.13);
    --border2:   rgba(255,255,255,0.2);
    --accent:    #8b5cf6;
    --accent2:   #3b82f6;
    --glow:      rgba(139,92,246,0.45);
    --text:      #f0ecfc;
    --muted:     rgba(255,255,255,0.58);
    --dim:       rgba(255,255,255,0.32);
    --green:     #6ee7b7;
    --blue:      #93c5fd;
    --pink:      #f9a8d4;
    --yellow:    #fde68a;
    --serif:     'DM Serif Display', Georgia, serif;
    --sans:      'DM Sans', system-ui, sans-serif;
    --radius:    18px;
    --radius-sm: 11px;
    --shadow:    0 20px 60px rgba(0,0,0,0.45);
}

*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }

body {
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
}

/* ── CANVAS BACKGROUND ── */
.canvas {
    position: fixed; inset: 0; z-index: 0;
    pointer-events: none; overflow: hidden;
}
.orb {
    position: absolute; border-radius: 50%;
    filter: blur(100px); mix-blend-mode: screen;
}
.orb-1 { width:700px;height:700px;background:#4c1d95;opacity:.55;top:-200px;left:-200px; animation: drift1 18s ease-in-out infinite alternate; }
.orb-2 { width:500px;height:500px;background:#1d4ed8;opacity:.45;bottom:-100px;right:-100px; animation: drift2 22s ease-in-out infinite alternate; }
.orb-3 { width:360px;height:360px;background:#5b21b6;opacity:.28;top:40%;left:55%; animation: drift3 15s ease-in-out infinite alternate; }

@keyframes drift1 { to { transform: translate(60px, 40px); } }
@keyframes drift2 { to { transform: translate(-40px, -60px); } }
@keyframes drift3 { to { transform: translate(-80px, 50px); } }

/* Grain overlay — lighter so bg shows through */
.canvas::after {
    content: '';
    position: absolute; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    opacity: .4;
}

/* ── GLASS CARD ── */
.glass {
    background: var(--surface);
    backdrop-filter: blur(28px) saturate(160%);
    -webkit-backdrop-filter: blur(28px) saturate(160%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,0.09);
    transition: border-color .3s, box-shadow .3s, transform .3s;
}
.glass:hover {
    border-color: rgba(139,92,246,0.45);
    box-shadow: var(--shadow), 0 0 0 1px rgba(139,92,246,0.15), inset 0 1px 0 rgba(255,255,255,0.12);
}
.glass-lift:hover { transform: translateY(-3px); }

/* ── SECTION LABEL ── */
.slabel {
    font-size: 10px; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: #a78bfa; margin-bottom: 18px;
    display: flex; align-items: center; gap: 8px;
}
.slabel::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(167,139,250,0.4), transparent);
}

/* ── GLOW BUTTON ── */
.btn-glow {
    display: inline-flex; align-items: center; justify-content: center;
    gap: 8px; padding: 14px 28px;
    font-family: var(--sans); font-size: 14px; font-weight: 600;
    color: #fff;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    border: none; border-radius: 14px; cursor: pointer;
    box-shadow: 0 8px 32px var(--glow), 0 0 0 1px rgba(139,92,246,0.3);
    transition: all .25s; text-decoration: none; letter-spacing: 0.3px;
}
.btn-glow:hover { opacity:.9; transform:translateY(-2px); box-shadow:0 16px 48px var(--glow), 0 0 0 1px rgba(139,92,246,0.5); }
.btn-glow:active { transform:translateY(0); }

/* ── GHOST BUTTON ── */
.btn-ghost {
    display: inline-flex; align-items: center; justify-content: center;
    padding: 13px 22px;
    font-family: var(--sans); font-size: 13px; font-weight: 600;
    color: var(--muted);
    background: var(--surface); border: 1px solid var(--border2);
    border-radius: 14px; cursor: pointer; text-decoration: none;
    transition: all .2s;
}
.btn-ghost:hover { color: var(--text); background: var(--surface2); border-color: rgba(255,255,255,0.28); }

/* ── STAT BOX ── */
.stat-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: var(--radius-sm);
    padding: 16px 18px;
    transition: all .25s;
}
.stat-box:hover { background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.35); }
.stat-lbl { font-size:10px;font-weight:600;color:var(--dim);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px; }
.stat-val { font-size:14px;font-weight:600;color:var(--text);line-height:1.3; }

/* ── POST ITEM ── */
.pitem {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: var(--radius-sm);
    padding: 18px 20px; margin-bottom: 10px;
    position: relative; overflow: hidden; transition: all .25s;
}
.pitem::before {
    content: ''; position: absolute;
    top:0;left:0;width:3px;height:100%;
    background: linear-gradient(180deg,#8b5cf6,#3b82f6);
    opacity: 0; transition: opacity .25s;
}
.pitem:hover { border-color: rgba(139,92,246,0.35); background: rgba(139,92,246,0.07); }
.pitem:hover::before { opacity: 1; }

/* ── TAGS ── */
.ptag { display:inline-block;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:3px 10px;border-radius:20px;margin-bottom:10px; }
.tag-li   { background:rgba(37,99,235,.18);border:1px solid rgba(37,99,235,.38);color:#93c5fd; }
.tag-ig   { background:rgba(236,72,153,.15);border:1px solid rgba(236,72,153,.35);color:#f9a8d4; }
.tag-tw   { background:rgba(14,165,233,.15);border:1px solid rgba(14,165,233,.35);color:#7dd3fc; }
.tag-idea { background:rgba(245,158,11,.14);border:1px solid rgba(245,158,11,.34);color:#fde68a; }

/* ── COPY BUTTON ── */
.copy-btn {
    font-size:11px;font-weight:600;font-family:var(--sans);
    color:var(--dim);background:rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.14);border-radius:8px;
    padding:5px 12px;cursor:pointer;transition:all .2s;
}
.copy-btn:hover { color:var(--text);background:rgba(139,92,246,.2);border-color:rgba(139,92,246,.45); }

/* ── TABS ── */
.tab-bar {
    display:flex;gap:4px;margin-bottom:18px;
    background:rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:5px;
}
.tab {
    flex:1;padding:10px 14px;font-size:12px;font-weight:600;
    font-family:var(--sans);color:var(--muted);
    background:none;border:none;border-radius:10px;
    cursor:pointer;transition:all .2s;text-align:center;
}
.tab:hover { color:rgba(255,255,255,.85);background:rgba(255,255,255,.07); }
.tab.active { color:#fff;background:linear-gradient(135deg,rgba(124,58,237,.65),rgba(37,99,235,.55));border:1px solid rgba(167,139,250,.35); }
.tab-panel { display:none; }
.tab-panel.active { display:block; animation: fadeUp .3s ease; }
@keyframes fadeUp { from { opacity:0;transform:translateY(6px); } to { opacity:1;transform:none; } }

/* ── PUBLISH BUTTONS ── */
.pub-li  { color:#93c5fd;background:rgba(37,99,235,.14);border:1px solid rgba(37,99,235,.32); }
.pub-li:hover  { background:rgba(37,99,235,.28);transform:translateY(-2px); }
.pub-ig  { color:#f9a8d4;background:rgba(236,72,153,.12);border:1px solid rgba(236,72,153,.28); }
.pub-ig:hover  { background:rgba(236,72,153,.26);transform:translateY(-2px); }
.pub-tw  { color:#7dd3fc;background:rgba(14,165,233,.12);border:1px solid rgba(14,165,233,.28); }
.pub-tw:hover  { background:rgba(14,165,233,.26);transform:translateY(-2px); }

/* ── BADGE PULSE ── */
.badge-active {
    display:inline-flex;align-items:center;gap:7px;
    background:rgba(110,231,183,.1);border:1px solid rgba(110,231,183,.28);
    color:var(--green);font-size:11px;font-weight:600;
    letter-spacing:1.5px;text-transform:uppercase;padding:6px 14px;border-radius:20px;
}
.pulse { width:7px;height:7px;background:var(--green);border-radius:50%;animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.35;transform:scale(.8)} }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(139,92,246,.5);border-radius:3px; }
</style>
"""


# ── HOME ──────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DropMeOnline — AI Growth Platform</title>
""" + DESIGN_SYSTEM + """
<style>
.page { position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px; }

/* Nav bar */
.nav { width:100%;max-width:720px;display:flex;align-items:center;justify-content:space-between;margin-bottom:60px; }
.nav-logo { font-family:var(--serif);font-size:20px;color:#fff;letter-spacing:-0.3px; }
.nav-link { font-size:12px;color:var(--muted);text-decoration:none;transition:color .2s; }
.nav-link:hover { color:var(--text); }

/* Hero */
.hero { width:100%;max-width:680px;text-align:center;margin-bottom:48px; }
.hero-eyebrow { display:inline-flex;align-items:center;gap:8px;background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.25);color:#c4b5fd;font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;padding:6px 16px;border-radius:20px;margin-bottom:28px; }
.hero-dot { width:6px;height:6px;background:var(--accent);border-radius:50%;animation:pulse 2s infinite; }
.hero-title { font-family:var(--serif);font-size:clamp(38px,6vw,64px);line-height:1.1;color:#fff;letter-spacing:-1px;margin-bottom:16px; }
.hero-title em { font-style:italic;background:linear-gradient(135deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.hero-sub { font-size:16px;color:var(--muted);line-height:1.7;max-width:520px;margin:0 auto; }

/* Command box */
.command-wrap { width:100%;max-width:680px;position:relative; }

.command-box {
    width:100%;
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,58,237,0.08), inset 0 1px 0 rgba(255,255,255,0.08);
    overflow: hidden;
    transition: border-color .3s, box-shadow .3s;
}
.command-box:focus-within {
    border-color: rgba(124,58,237,0.45);
    box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,58,237,0.2), 0 0 40px rgba(124,58,237,0.12), inset 0 1px 0 rgba(255,255,255,0.1);
}

.command-header { padding:18px 22px 0;display:flex;align-items:center;gap:8px; }
.cmd-dot { width:8px;height:8px;border-radius:50%; }
.cmd-dot:nth-child(1){background:#ff5f57;}
.cmd-dot:nth-child(2){background:#febc2e;}
.cmd-dot:nth-child(3){background:#28c840;}

.cmd-label { margin-left:auto;font-size:11px;color:var(--dim);letter-spacing:1px;text-transform:uppercase; }

.command-textarea {
    width:100%;min-height:130px;max-height:300px;
    padding:18px 22px 14px;
    font-family:var(--sans);font-size:15px;font-weight:400;
    color:var(--text);line-height:1.7;
    background:none;border:none;outline:none;resize:none;
    overflow-y:auto;
}
.command-textarea::placeholder { color:rgba(255,255,255,.2);font-style:italic; }

.command-footer {
    padding:14px 18px;
    display:flex;align-items:center;justify-content:space-between;
    border-top:1px solid rgba(255,255,255,.06);
    gap:12px;
}

/* File upload area */
.upload-zone {
    display:flex;align-items:center;gap:8px;
    padding:7px 14px;
    background:rgba(255,255,255,.03);
    border:1px dashed rgba(255,255,255,.1);
    border-radius:10px;cursor:pointer;
    transition:all .2s;position:relative;overflow:hidden;
}
.upload-zone:hover { background:rgba(124,58,237,.08);border-color:rgba(124,58,237,.3); }
.upload-zone input[type=file] { position:absolute;inset:0;opacity:0;cursor:pointer; }
.upload-icon { font-size:14px; }
.upload-label { font-size:12px;font-weight:500;color:var(--muted); }
#file-name { font-size:11px;color:var(--accent);max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap; }

/* Submit btn */
.submit-row { display:flex;align-items:center;gap:10px; }
.char-count { font-size:11px;color:var(--dim); }

/* Hint chips */
.chips { display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;width:100%;max-width:680px; }
.chip {
    padding:7px 14px;font-size:12px;font-weight:500;color:var(--muted);
    background:rgba(255,255,255,.03);border:1px solid var(--border);
    border-radius:20px;cursor:pointer;transition:all .2s;
}
.chip:hover { color:var(--text);background:rgba(124,58,237,.1);border-color:rgba(124,58,237,.3); }

/* Footer nav */
.bottom-nav { display:flex;gap:20px;margin-top:52px;opacity:.5; }
.bottom-nav a { font-size:12px;color:var(--muted);text-decoration:none;transition:color .2s; }
.bottom-nav a:hover { color:var(--text);opacity:1; }
</style>
</head>
<body>
<div class="canvas">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
</div>

<div class="page">
    <nav class="nav">
        <span class="nav-logo">DropMeOnline</span>
        <a href="/memory" class="nav-link">Memory →</a>
    </nav>

    <div class="hero">
        <div class="hero-eyebrow"><span class="hero-dot"></span>AI Growth Platform</div>
        <h1 class="hero-title">Your brand,<br><em>on autopilot.</em></h1>
        <p class="hero-sub">Describe your product, audience, and goal. The AI builds your full social media strategy, content calendar, and viral posts — instantly.</p>
    </div>

    <div class="command-wrap">
        <form action="/generate-strategy" method="post" enctype="multipart/form-data">
            <div class="command-box" id="cmdBox">
                <div class="command-header">
                    <span class="cmd-dot"></span><span class="cmd-dot"></span><span class="cmd-dot"></span>
                    <span class="cmd-label">Strategy Prompt</span>
                </div>
                <textarea
                    class="command-textarea"
                    id="goalTextarea"
                    name="goal"
                    rows="5"
                    placeholder="Grow my AI resume tool for 30 days on LinkedIn, Instagram and Twitter. Tone: bold + smart. Audience: freshers. Use meme style for Instagram."
                    required
                    oninput="updateChar(this)"
                ></textarea>
                <div class="command-footer">
                    <div class="upload-zone">
                        <input type="file" id="inspirationFile" name="inspiration" accept="image/*,.pdf,.txt" onchange="showFile(this)">
                        <span class="upload-icon">＋</span>
                        <span class="upload-label">Attach inspiration</span>
                        <span id="file-name"></span>
                    </div>
                    <div class="submit-row">
                        <span class="char-count" id="charCount">0</span>
                        <button type="submit" class="btn-glow">
                            Generate Strategy
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                        </button>
                    </div>
                </div>
            </div>
        </form>

        <div class="chips">
            <span class="chip" onclick="fillChip('Grow my AI tool on LinkedIn for 30 days. Audience: developers.')">🤖 AI tool</span>
            <span class="chip" onclick="fillChip('Promote my SaaS product on Twitter and LinkedIn. Bold tone. Founders audience.')">🚀 SaaS launch</span>
            <span class="chip" onclick="fillChip('Build personal brand on Instagram and LinkedIn. Career niche. Freshers audience.')">👤 Personal brand</span>
            <span class="chip" onclick="fillChip('Market my online course on Instagram. Gen Z audience. Meme style.')">📚 Online course</span>
            <span class="chip" onclick="fillChip('Grow fitness brand on Instagram and TikTok. Motivational tone.')">💪 Fitness brand</span>
        </div>
    </div>

    <div class="bottom-nav">
        <a href="/memory">Past strategies</a>
        <span style="color:var(--dim)">·</span>
        <span style="font-size:12px;color:var(--dim);">Powered by DropMeOnline AI</span>
    </div>
</div>

<script>
function updateChar(el) {
    document.getElementById('charCount').textContent = el.value.length;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 300) + 'px';
}
function showFile(input) {
    const name = input.files[0] ? input.files[0].name : '';
    document.getElementById('file-name').textContent = name ? '· ' + name : '';
}
function fillChip(text) {
    const ta = document.getElementById('goalTextarea');
    ta.value = text;
    ta.focus();
    updateChar(ta);
}
</script>
</body>
</html>"""


# ── GENERATE STRATEGY ─────────────────────────────────────────────────────────
@app.post("/generate-strategy", response_class=HTMLResponse)
def generate(goal: str = Form(...)):

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
    images       = generate_images(goal, result["niche"], mind.get("tone",""), mind)
    market       = analyze_market(goal)
    publish      = build_publish_queue(campaign, active_platforms)

    def safe(val):
        return str(val).replace("{","").replace("}","").replace("'","&#39;").replace('"','&quot;')

    def sraw(val):
        return str(val).replace("{","").replace("}","")

    # Image SVGs
    li_svg  = images["linkedin"]["svg"]
    ig_svg  = images["instagram"]["svg"]
    tw_svg  = images["twitter"]["svg"]
    li_img_prompt = sraw(images["linkedin"]["prompt"])
    ig_img_prompt = sraw(images["instagram"]["prompt"])
    tw_img_prompt = sraw(images["twitter"]["prompt"])
    img_style     = sraw(images["linkedin"]["style"])

    days_of_week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    cal_rows = ""
    for i, item in enumerate(campaign[:7]):
        cal_rows += f"""<div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.04);">
            <div style="min-width:32px;font-family:var(--serif);font-size:18px;color:var(--accent);font-weight:700;">{item['day']}</div>
            <div><div style="font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:1px;">{days_of_week[i%7]}</div>
            <div style="font-size:12px;color:var(--muted);margin-top:2px;">{sraw(item['theme'])} — {sraw(item['hook'])[:55]}...</div></div>
        </div>"""

    li_post_1  = sraw(auto_content["post"])
    li_post_2  = sraw(adapted.get("linkedin",""))
    ig_post_1  = sraw(adapted.get("instagram",""))
    ig_post_2  = sraw(content.get("instagram",""))
    tw_tweet_1 = sraw(adapted.get("twitter",""))
    tw_tweet_2 = sraw(auto_content["hook"])
    tw_tweet_3 = sraw(auto_content["cta"])
    li_carousel= sraw(visuals.get("headline",""))
    ig_reel    = "Reel: " + sraw(visuals.get("image_prompt",""))[:100] + "..."
    ig_story   = "Story: " + sraw(auto_content.get("image_idea",""))[:100] + "..."
    tw_thread  = sraw(mind["top_hooks"][0]) if mind.get("top_hooks") else sraw(auto_content["hook"])
    li_url     = links.get("linkedin_url","#")
    tw_url     = links.get("twitter_url","#")

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard — DropMeOnline</title>
""" + DESIGN_SYSTEM + """
<style>
.page   { position:relative;z-index:1;max-width:1140px;margin:0 auto;padding:0 20px 80px; }
.header { padding:24px 0;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,.05);margin-bottom:36px; }
.h-left { display:flex;align-items:center;gap:12px; }
.logo   { font-family:var(--serif);font-size:19px;color:#fff;letter-spacing:-0.3px; }
.goal-pill { font-size:12px;color:var(--dim);max-width:380px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap; }

/* Stats row */
.stats-row { display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px; }
.sstat { padding:20px;border-left:3px solid transparent;transition:all .3s; }
.sstat:hover { border-left-color:var(--accent); }
.sstat .n  { font-family:var(--serif);font-size:32px;color:#fff;line-height:1; }
.sstat .lb { font-size:11px;color:var(--dim);text-transform:uppercase;letter-spacing:1.5px;margin-top:6px; }

/* Action center */
.action-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:12px; }

/* Main layout */
.main-grid { display:grid;grid-template-columns:1fr 330px;gap:22px;align-items:start; }
.left-col,.right-col { display:flex;flex-direction:column;gap:18px; }

/* Visual grid */
.vgrid  { display:grid;grid-template-columns:1fr 1fr;gap:12px; }
.vfull  { grid-column:span 2; }
.vstat  { background:rgba(255,255,255,.025);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px 16px; }
.vlbl   { font-size:10px;font-weight:600;color:var(--dim);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px; }
.vval   { font-size:13px;color:#c4b5fd;line-height:1.6; }

/* Pub row */
.pub-row { display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px; }
.pub-btn { display:block;text-align:center;padding:13px;font-size:12px;font-weight:600;font-family:var(--sans);border-radius:12px;text-decoration:none;cursor:pointer;transition:all .25s;border:none; }

/* Strategy intel */
.intel-note { margin-top:14px;padding:14px 16px;background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:var(--radius-sm);font-size:12px;color:var(--muted);line-height:1.7; }

/* Feedback form */
.fform select {
    width:100%;padding:10px 14px;font-size:13px;font-family:var(--sans);
    color:var(--text);background:rgba(255,255,255,.04);
    border:1px solid var(--border2);border-radius:var(--radius-sm);outline:none;margin-top:4px;
    appearance:none;cursor:pointer;
}
.fform .fgrid { display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px; }
.fform label  { font-size:11px;font-weight:600;color:var(--dim);text-transform:uppercase;letter-spacing:1px; }

/* Back */
.back { display:inline-flex;align-items:center;gap:6px;color:var(--dim);font-size:12px;text-decoration:none;transition:color .2s; }
.back:hover { color:#a78bfa; }

/* Responsive */
@media(max-width:960px){ .main-grid{grid-template-columns:1fr} .stats-row{grid-template-columns:1fr 1fr} .action-grid{grid-template-columns:1fr 1fr} .pub-row{grid-template-columns:1fr} }
@media(max-width:520px){ .stats-row{grid-template-columns:1fr 1fr} .action-grid{grid-template-columns:1fr} }
</style>
</head>
<body>
<div class="canvas"><div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div></div>
<div class="page">

<!-- HEADER -->
<div class="header">
    <div class="h-left">
        <span class="logo">DropMeOnline</span>
        <span style="color:var(--dim);font-size:16px;">·</span>
        <span class="goal-pill">""" + safe(goal) + """</span>
    </div>
    <div class="badge-active"><span class="pulse"></span>Autopilot Active</div>
</div>

<!-- STATS ROW -->
<div class="stats-row" style="margin-bottom:22px;">
    <div class="glass sstat"><div class="n">""" + str(stats["posts_generated"]) + """</div><div class="lb">Posts Generated</div></div>
    <div class="glass sstat"><div class="n">""" + str(stats["campaigns_created"]) + """</div><div class="lb">Campaigns</div></div>
    <div class="glass sstat"><div class="n" style="font-size:26px;color:var(--green);">""" + str(stats["growth_score"]) + """</div><div class="lb">Growth Score</div></div>
    <div class="glass sstat"><div class="n" style="color:#a78bfa;">""" + str(stats.get("streak_days",1)) + """d</div><div class="lb">Active Streak</div></div>
</div>

<!-- ACTION CENTER -->
<div class="glass" style="padding:26px;margin-bottom:22px;">
    <div class="slabel">Today's Action Center</div>
    <div class="action-grid">
        <div class="stat-box"><div class="stat-lbl">Best Platform</div><div class="stat-val" style="color:#a78bfa;">""" + safe(stats["best_platform_today"]) + """</div></div>
        <div class="stat-box"><div class="stat-lbl">Post Time</div><div class="stat-val" style="color:var(--green);">""" + safe(brain["next_post_time"]) + """</div></div>
        <div class="stat-box"><div class="stat-lbl">Content Type</div><div class="stat-val" style="color:var(--blue);">""" + safe(growth["content_type"]) + """</div></div>
        <div class="stat-box"><div class="stat-lbl">Next Action</div><div class="stat-val" style="font-size:11px;color:var(--muted);line-height:1.4;">""" + safe(stats["next_action"])[:75] + """…</div></div>
    </div>
</div>

<div class="main-grid">
<div class="left-col">

<!-- PLATFORM TABS -->
<div class="glass" style="padding:26px;">
    <div class="slabel">Platform Content</div>
    <div class="tab-bar">
        <button class="tab active" onclick="switchTab('linkedin',this)">LinkedIn</button>
        <button class="tab" onclick="switchTab('instagram',this)">Instagram</button>
        <button class="tab" onclick="switchTab('twitter',this)">Twitter / X</button>
    </div>

    <div id="tab-linkedin" class="tab-panel active">
        <div class="pitem">
            <span class="ptag tag-li">Post 1 — Autopilot</span>
            <div style="font-size:13px;color:var(--muted);line-height:1.75;white-space:pre-line;">""" + li_post_1[:380] + """</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
                <span style="font-size:11px;color:var(--dim);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + li_post_1.replace("'","").replace('"',"")[:320] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-li">Post 2 — Adapted</span>
            <div style="font-size:13px;color:var(--muted);line-height:1.75;white-space:pre-line;">""" + li_post_2[:380] + """</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
                <span style="font-size:11px;color:var(--dim);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + li_post_2.replace("'","").replace('"',"")[:320] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem"><span class="ptag tag-idea">Carousel Idea</span><div style="font-size:13px;color:var(--muted);line-height:1.6;">""" + li_carousel[:180] + """</div></div>
    </div>

    <div id="tab-instagram" class="tab-panel">
        <div class="pitem">
            <span class="ptag tag-ig">Caption 1</span>
            <div style="font-size:13px;color:var(--muted);line-height:1.75;white-space:pre-line;">""" + ig_post_1[:380] + """</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
                <span style="font-size:11px;color:var(--dim);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + ig_post_1.replace("'","").replace('"',"")[:320] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-ig">Caption 2</span>
            <div style="font-size:13px;color:var(--muted);line-height:1.75;white-space:pre-line;">""" + ig_post_2[:380] + """</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
                <span style="font-size:11px;color:var(--dim);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + ig_post_2.replace("'","").replace('"',"")[:320] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem"><span class="ptag tag-idea">Reel Idea</span><div style="font-size:13px;color:var(--muted);">""" + ig_reel[:180] + """</div></div>
        <div class="pitem"><span class="ptag tag-idea">Story Idea</span><div style="font-size:13px;color:var(--muted);">""" + ig_story[:180] + """</div></div>
    </div>

    <div id="tab-twitter" class="tab-panel">
        <div class="pitem">
            <span class="ptag tag-tw">Tweet 1 — Bold</span>
            <div style="font-size:13px;color:var(--muted);line-height:1.75;">""" + tw_tweet_1[:280] + """</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
                <span style="font-size:11px;color:var(--dim);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + tw_tweet_1.replace("'","").replace('"',"")[:250] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem">
            <span class="ptag tag-tw">Tweet 2 — Hook</span>
            <div style="font-size:13px;color:var(--muted);line-height:1.75;">""" + tw_tweet_2[:280] + """</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
                <span style="font-size:11px;color:var(--dim);">Ready</span>
                <button class="copy-btn" onclick="cp(this,'""" + tw_tweet_2.replace("'","").replace('"',"")[:250] + """')">Copy</button>
            </div>
        </div>
        <div class="pitem"><span class="ptag tag-tw">Tweet 3 — CTA</span><div style="font-size:13px;color:var(--muted);">""" + tw_tweet_3[:280] + """</div></div>
        <div class="pitem"><span class="ptag tag-idea">Thread Hook</span><div style="font-size:13px;color:var(--muted);">""" + sraw(tw_thread)[:200] + """</div></div>
    </div>
</div>

<!-- PUBLISH -->
<div class="glass" style="padding:26px;">
    <div class="slabel">Publish Now</div>
    <div class="pub-row">
        <a href='""" + li_url + """' target="_blank" class="pub-btn pub-li">→ LinkedIn</a>
        <button class="pub-btn pub-ig" onclick="alert('Copy caption above, then open Instagram.')">→ Instagram</button>
        <a href='""" + tw_url + """' target="_blank" class="pub-btn pub-tw">→ Twitter / X</a>
    </div>
</div>

<!-- STRATEGY INTEL -->
<div class="glass" style="padding:26px;">
    <div class="slabel">Strategy Intelligence</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
        <div class="stat-box"><div class="stat-lbl">Niche</div><div class="stat-val">""" + safe(result["niche"]) + """</div></div>
        <div class="stat-box"><div class="stat-lbl">Trigger</div><div class="stat-val" style="color:#c4b5fd;">""" + safe(mind["psychology_trigger"]) + """</div></div>
        <div class="stat-box"><div class="stat-lbl">Tone</div><div class="stat-val" style="font-size:12px;">""" + safe(flow["tone_lock"])[:55] + """</div></div>
        <div class="stat-box"><div class="stat-lbl">LI Frequency</div><div class="stat-val" style="color:var(--green);">""" + safe(plan["linkedin_frequency"]) + """</div></div>
    </div>
    <div class="intel-note">""" + safe(flow["content_strategy"])[:280] + """</div>
</div>

<!-- FEEDBACK FORM -->
<div class="glass" style="padding:26px;">
    <div class="slabel">Update AI Learning</div>
    <form action="/update-feedback" method="post" class="fform">
        <input type="hidden" name="platform" value="linkedin">
        <div class="fgrid">
            <div><label>Reach</label><select name="reach"><option value="high">High</option><option value="medium" selected>Medium</option><option value="low">Low</option></select></div>
            <div><label>Likes</label><select name="likes"><option value="high">High</option><option value="medium" selected>Medium</option><option value="low">Low</option></select></div>
            <div><label>Comments</label><select name="comments"><option value="high">High</option><option value="medium" selected>Medium</option><option value="low">Low</option></select></div>
            <div><label>Overall</label><select name="overall"><option value="good">Good</option><option value="average" selected>Average</option><option value="bad">Bad</option></select></div>
        </div>
        <button type="submit" class="btn-glow" style="width:100%;">Update AI Learning →</button>
    </form>
</div>

</div><!-- end left-col -->

<!-- RIGHT COLUMN -->
<div class="right-col">

<!-- VISUAL ASSETS -->
<div class="glass" style="padding:24px;">
    <div class="slabel">Visual Assets</div>
    <style>
    .img-card{position:relative;border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.1);margin-bottom:14px;cursor:zoom-in;transition:transform .25s,box-shadow .25s;}
    .img-card:hover{transform:scale(1.015);box-shadow:0 16px 48px rgba(0,0,0,0.6);}
    .img-card svg{display:block;width:100%;height:auto;}
    .img-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.75) 0%,transparent 50%);opacity:0;transition:opacity .25s;}
    .img-card:hover .img-overlay{opacity:1;}
    .img-actions{position:absolute;bottom:12px;left:12px;right:12px;display:flex;gap:8px;opacity:0;transition:opacity .25s;}
    .img-card:hover .img-actions{opacity:1;}
    .img-btn{flex:1;padding:7px 10px;font-size:11px;font-weight:600;font-family:var(--sans);border-radius:8px;border:none;cursor:pointer;transition:all .2s;text-align:center;}
    .img-btn-dl{background:rgba(255,255,255,0.15);color:#fff;backdrop-filter:blur(8px);}
    .img-btn-cp{background:rgba(139,92,246,0.3);color:#c4b5fd;backdrop-filter:blur(8px);}
    .img-btn-dl:hover{background:rgba(255,255,255,0.25);}
    .img-btn-cp:hover{background:rgba(139,92,246,0.5);}
    .img-plat-tag{position:absolute;top:10px;left:10px;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:3px 10px;border-radius:20px;backdrop-filter:blur(8px);}
    </style>

    <!-- LinkedIn Image -->
    <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">LinkedIn</div>
    <div class="img-card" id="li-img-card">
        """ + li_svg + """
        <div class="img-overlay"></div>
        <span class="img-plat-tag tag-li">LinkedIn Cover</span>
        <div class="img-actions">
            <button class="img-btn img-btn-dl" onclick="dlSvg('li-img-card','linkedin-cover.svg')">⬇ Download</button>
            <button class="img-btn img-btn-cp" onclick="cpPrompt('""" + li_img_prompt[:200].replace("'","").replace('"','') + """')">Copy Prompt</button>
        </div>
    </div>

    <!-- Instagram Image -->
    <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Instagram</div>
    <div class="img-card" id="ig-img-card">
        """ + ig_svg + """
        <div class="img-overlay"></div>
        <span class="img-plat-tag tag-ig">Instagram Post</span>
        <div class="img-actions">
            <button class="img-btn img-btn-dl" onclick="dlSvg('ig-img-card','instagram-post.svg')">⬇ Download</button>
            <button class="img-btn img-btn-cp" onclick="cpPrompt('""" + ig_img_prompt[:200].replace("'","").replace('"','') + """')">Copy Prompt</button>
        </div>
    </div>

    <!-- Twitter Image -->
    <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Twitter / X</div>
    <div class="img-card" id="tw-img-card">
        """ + tw_svg + """
        <div class="img-overlay"></div>
        <span class="img-plat-tag tag-tw">Twitter Card</span>
        <div class="img-actions">
            <button class="img-btn img-btn-dl" onclick="dlSvg('tw-img-card','twitter-card.svg')">⬇ Download</button>
            <button class="img-btn img-btn-cp" onclick="cpPrompt('""" + tw_img_prompt[:200].replace("'","").replace('"','') + """')">Copy Prompt</button>
        </div>
    </div>

    <div style="font-size:11px;color:rgba(255,255,255,0.25);margin-top:4px;line-height:1.5;">Style: <span style="color:#a78bfa;">""" + img_style + """</span> · SVG — download and use directly, or copy prompt for AI generators (Firefly, Canva AI, Leonardo)</div>
</div>

<!-- 7 DAY CALENDAR -->
<div class="glass" style="padding:24px;">
    <div class="slabel">7-Day Calendar</div>
    """ + cal_rows + """
</div>

<!-- TREND RADAR -->
<div class="glass" style="padding:24px;">
    <div class="slabel">Trend Radar</div>
    <div style="font-size:12px;font-weight:600;color:#a78bfa;margin-bottom:8px;">Best topic today</div>
    <div style="font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:16px;padding:12px;background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.12);border-radius:10px;">""" + safe(trends["best_topic_today"]) + """</div>
    <div style="font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:10px;">Hot topics</div>
    """ + "".join(f'<div style="padding:9px 12px;margin-bottom:7px;background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:9px;font-size:12px;color:var(--muted);">{safe(x)[:85]}</div>' for x in trends["hot_topics"][:3]) + """
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
        const orig=btn.textContent;
        btn.textContent='Copied!';btn.style.color='var(--green)';
        setTimeout(()=>{btn.textContent=orig;btn.style.color='';},2000);
    });
}
function dlSvg(cardId, filename){
    const card = document.getElementById(cardId);
    const svg  = card.querySelector('svg');
    if(!svg) return;
    const blob = new Blob([svg.outerHTML], {type:'image/svg+xml'});
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url; a.download = filename;
    a.click(); URL.revokeObjectURL(url);
}
function cpPrompt(text){
    navigator.clipboard.writeText(text).then(()=>{
        const btns = document.querySelectorAll('.img-btn-cp');
        btns.forEach(b=>{ if(b.onclick && b.onclick.toString().includes(text.slice(0,20))){ b.textContent='Copied!'; setTimeout(()=>b.textContent='Copy Prompt',2000); } });
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
    decision    = result["decision"]
    badge_class = "badge-keep" if decision == "keep" else "badge-change"

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Learning Updated — DropMeOnline</title>
""" + DESIGN_SYSTEM + """
<style>
.page{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px 20px;position:relative;z-index:1;}
.wrap{max-width:500px;width:100%;}
.banner{background:linear-gradient(135deg,rgba(109,40,217,.25),rgba(37,99,235,.2));border:1px solid rgba(167,139,250,.18);border-radius:20px;padding:28px;text-align:center;margin-bottom:20px;box-shadow:0 0 60px rgba(109,40,217,.12);}
.icon{font-size:36px;display:block;margin-bottom:10px;}
.ttl{font-family:var(--serif);font-size:26px;color:#fff;margin-bottom:5px;}
.sub{font-size:13px;color:var(--muted);}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.full{grid-column:span 2;}
.badge-keep{background:rgba(110,231,183,.1);border:1px solid rgba(110,231,183,.25);color:var(--green);display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.badge-change{background:rgba(252,165,165,.1);border:1px solid rgba(252,165,165,.25);color:#fca5a5;display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.style-val{font-size:13px;color:#c4b5fd;line-height:1.6;}
.row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px;}
.back{display:inline-flex;color:var(--dim);font-size:12px;text-decoration:none;margin-bottom:22px;transition:color .2s;}
.back:hover{color:#a78bfa;}
</style>
</head>
<body>
<div class="canvas"><div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div></div>
<div class="page"><div class="wrap">
<a href="/" class="back">← Back</a>
<div class="banner"><span class="icon">🧠</span><div class="ttl">AI Learning Updated</div><div class="sub">Strategy adjusted based on your feedback</div></div>
<div class="glass" style="padding:28px;">
    <div class="slabel">Updated Strategy</div>
    <div class="grid">
        <div class="stat-box"><div class="stat-lbl">Platform</div><div class="stat-val">""" + str(platform) + """</div></div>
        <div class="stat-box"><div class="stat-lbl">Decision</div><div class="stat-val"><span class='""" + badge_class + """'>""" + decision.upper() + """</span></div></div>
        <div class="stat-box"><div class="stat-lbl">Next Post Time</div><div class="stat-val">""" + str(result["next_time"]) + """</div></div>
        <div class="stat-box"><div class="stat-lbl">Frequency</div><div class="stat-val">""" + str(result["frequency"]) + """</div></div>
        <div class="stat-box full"><div class="stat-lbl">Recommended Style</div><div class="style-val">""" + str(result["content_style"]) + """</div></div>
    </div>
</div>
<div class="row" style="margin-top:16px;">
    <a href="/" class="btn-ghost">← Home</a>
    <a href="/" class="btn-glow" style="width:100%;justify-content:center;">New Strategy →</a>
</div>
</div></div></body></html>"""


# ── MEMORY ────────────────────────────────────────────────────────────────────
@app.get("/memory", response_class=HTMLResponse)
def view_memory():
    memory = get_memory()
    items = ""
    for item in memory:
        goal_text = item["goal"] if isinstance(item, dict) and "goal" in item else str(item)[:80]
        items += f"""<div class="glass glass-lift" style="padding:16px 20px;margin-bottom:10px;cursor:pointer;" onclick="window.location='/'">
            <div style="font-size:13px;color:var(--muted);line-height:1.5;">{goal_text}</div>
        </div>"""

    empty = '<div style="font-size:13px;color:var(--dim);padding:20px 0;">No strategies yet — generate your first one.</div>'

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Memory — DropMeOnline</title>
""" + DESIGN_SYSTEM + """
<style>
.page{min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:60px 20px;position:relative;z-index:1;}
.wrap{max-width:580px;width:100%;}
.h{font-family:var(--serif);font-size:28px;color:#fff;margin-bottom:28px;letter-spacing:-0.5px;}
.back{display:inline-flex;color:var(--dim);font-size:12px;text-decoration:none;margin-bottom:28px;transition:color .2s;}
.back:hover{color:#a78bfa;}
</style>
</head>
<body>
<div class="canvas"><div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div></div>
<div class="page"><div class="wrap">
<a href="/" class="back">← Back to Home</a>
<div class="h">Past Strategies</div>
""" + (items if items else empty) + """
</div></div></body></html>"""