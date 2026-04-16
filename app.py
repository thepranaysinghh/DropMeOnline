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

app = FastAPI()


# 🏠 Home Page
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DropMeOnline</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
 
        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            padding: 20px;
        }
 
        /* Soft ambient blobs */
        body::before, body::after {
            content: '';
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.25;
            pointer-events: none;
        }
 
        body::before {
            width: 400px;
            height: 400px;
            background: #7c3aed;
            top: -100px;
            left: -100px;
        }
 
        body::after {
            width: 350px;
            height: 350px;
            background: #2563eb;
            bottom: -80px;
            right: -80px;
        }
 
        /* Glass card */
        .card {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 48px 40px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        }
 
        /* Badge */
        .badge {
            display: inline-block;
            background: rgba(124, 58, 237, 0.3);
            border: 1px solid rgba(124, 58, 237, 0.5);
            color: #c4b5fd;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 20px;
            margin-bottom: 20px;
        }
 
        h1 {
            font-size: 28px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
            line-height: 1.3;
        }
 
        .subtitle {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.45);
            margin-bottom: 36px;
            line-height: 1.6;
        }
 
        /* Label */
        label {
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.5);
            letter-spacing: 0.8px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
 
        /* Input */
        input[type="text"] {
            width: 100%;
            padding: 14px 18px;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            outline: none;
            transition: border-color 0.2s;
            margin-bottom: 20px;
        }
 
        input[type="text"]::placeholder {
            color: rgba(255, 255, 255, 0.25);
        }
 
        input[type="text"]:focus {
            border-color: rgba(124, 58, 237, 0.6);
            background: rgba(255, 255, 255, 0.09);
        }
 
        /* Button */
        button {
            width: 100%;
            padding: 14px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            border: none;
            border-radius: 12px;
            cursor: pointer;
            letter-spacing: 0.3px;
            transition: opacity 0.2s, transform 0.1s;
        }
 
        button:hover {
            opacity: 0.88;
            transform: translateY(-1px);
        }
 
        button:active {
            transform: translateY(0);
        }
 
        /* Divider */
        .divider {
            height: 1px;
            background: rgba(255, 255, 255, 0.08);
            margin: 28px 0;
        }
 
        /* Memory link */
        .memory-link {
            text-align: center;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.35);
        }
 
        .memory-link a {
            color: #a78bfa;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
 
        .memory-link a:hover {
            color: #c4b5fd;
        }
    </style>
</head>
<body>
 
<div class="card">
    <div class="section-label">Strategy</div>

    <div class="strategy-grid">
        <div class="stat-box">
            <div class="stat-label">Niche</div>
            <div class="stat-value">{result['niche']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Tone</div>
            <div class="stat-value">{result['tone']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Posting</div>
            <div class="stat-value">{result['posting_frequency']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Goal</div>
            <div class="stat-value">{result['goal']}</div>
        </div>
    </div>
</div>

    <div class="card">

    <div class="card">
 
        <div class="badge">AI Strategist</div>
 
        <h1>DropMeOnline</h1>
        <p class="subtitle">Your personal AI-powered social media strategist. Enter a goal and let the engine do the rest.</p>
 
        <form action="/generate-strategy" method="post">
            <label for="goal">Your Goal</label>
            <input
                type="text"
                id="goal"
                name="goal"
                placeholder="e.g. Grow AI niche for 30 days"
                required
            />
            <button type="submit">Generate Strategy →</button>
        </form>
 
        <div class="divider"></div>
 
        <div class="memory-link">
            View past strategies → <a href="/memory">Memory</a>
        </div>
 
    </div>
 
</body>
</html>
 
    """


# 🚀 Generate Strategy
@app.post("/generate-strategy", response_class=HTMLResponse)
def generate(goal: str = Form(...)):
    result = generate_strategy(goal)
    save_memory(result)

    content = generate_content(goal)
    plan = decide_post_plan(goal)
    growth = decide_growth_strategy(goal, "linkedin", {"engagement": "high", "last_posts": 5})
    adapted = adapt_platform(content)
    links = generate_publish_links(content)
    variations = generate_variations(goal)

    return f"""
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strategy — DropMeOnline</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    padding: 40px 20px;
}}

body::before, body::after {{
    content: '';
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.2;
    pointer-events: none;
}}

body::before {{
    width: 400px;
    height: 400px;
    background: #7c3aed;
    top: -100px;
    left: -100px;
}}

body::after {{
    width: 350px;
    height: 350px;
    background: #2563eb;
    bottom: -80px;
    right: -80px;
}}

.wrapper {{
    max-width: 640px;
    margin: 0 auto;
}}

.back {{
    display: inline-block;
    color: rgba(255,255,255,0.4);
    font-size: 13px;
    text-decoration: none;
    margin-bottom: 28px;
    transition: color 0.2s;
}}

.back:hover {{ color: #a78bfa; }}

.card {{
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}}

.section-label {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 14px;
}}

.goal-text {{
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
    line-height: 1.4;
}}

.strategy-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 4px;
}}

.stat-box {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 16px;
}}

.stat-label {{
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}}

.stat-value {{
    font-size: 14px;
    font-weight: 500;
    color: #e2e8f0;
}}

.platform-tag {{
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 12px;
}}

.tag-linkedin {{ background: rgba(37,99,235,0.25); color: #93c5fd; border: 1px solid rgba(37,99,235,0.4); }}
.tag-instagram {{ background: rgba(236,72,153,0.2); color: #f9a8d4; border: 1px solid rgba(236,72,153,0.35); }}
.tag-twitter {{ background: rgba(14,165,233,0.2); color: #7dd3fc; border: 1px solid rgba(14,165,233,0.35); }}

.post-text {{
    font-size: 14px;
    color: rgba(255,255,255,0.75);
    line-height: 1.8;
    white-space: pre-line;
}}

.divider {{
    height: 1px;
    background: rgba(255,255,255,0.07);
    margin: 20px 0;
}}

.variation-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
}}

.variation-list li {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 14px;
    color: rgba(255,255,255,0.7);
    line-height: 1.5;
}}

.variation-list li::before {{
    content: '→ ';
    color: #a78bfa;
    font-weight: 600;
}}

.btn-home {{
    display: block;
    text-align: center;
    margin-top: 8px;
    padding: 14px;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    color: #ffffff;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    border-radius: 12px;
    text-decoration: none;
    transition: opacity 0.2s, transform 0.1s;
}}

.btn-home:hover {{
    opacity: 0.88;
    transform: translateY(-1px);
}}
</style>
 
<div class="wrapper">
 
    <a href="/" class="back">← Back to Home</a>
 
    <!-- Goal Card -->
    <div class="card">
        <div class="section-label">Your Goal</div>
        <div class="goal-text">{result['goal']}</div>
    </div>
 
    <!-- Strategy Card -->
    <div class="card">
        <div class="section-label">Strategy Overview</div>
        <div class="strategy-grid">
            <div class="stat-box">
                <div class="stat-label">Niche</div>
                <div class="stat-value">{result['niche']}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Tone</div>
                <div class="stat-value">{result['tone']}</div>
            </div>
            <div class="stat-box" style="grid-column: span 2;">
                <div class="stat-label">Posting Frequency</div>
                <div class="stat-value">{result['posting_frequency']}</div>
            </div>
        </div>
    </div>

    <div class="card">
    <div class="section-label">Posting Plan</div>

    <div class="card">
    <div class="section-label">Growth Strategy</div>

    <div class="strategy-grid">
        <div class="stat-box">
            <div class="stat-label">Frequency</div>
            <div class="stat-value">{growth['posting_frequency']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Content Type</div>
            <div class="stat-value">{growth['content_type']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Hook Style</div>
            <div class="stat-value">{growth['hook_style']}</div>
        </div>
    </div>

    <div class="divider"></div>

    <div class="post-text">{growth['notes']}</div>
</div>

    <div class="strategy-grid">
        <div class="stat-box">
            <div class="stat-label">LinkedIn</div>
            <div class="stat-value">{plan['linkedin_frequency']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Instagram</div>
            <div class="stat-value">{plan['instagram_frequency']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Twitter</div>
            <div class="stat-value">{plan['twitter_frequency']}</div>
        </div>
    </div>

    <div class="divider"></div>

    <div class="post-text">{plan['reasoning']}</div>
</div>
 
    <!-- Content Card -->
   <div class="card">
    <div class="section-label">Content</div>

    <div class="platform-tag tag-linkedin">LinkedIn</div>
    <div class="post-text">{content['linkedin']}</div>

    <div class="divider"></div>

    <div class="platform-tag tag-instagram">Instagram</div>
    <div class="post-text">{content['instagram']}</div>

    <div class="divider"></div>

    <div class="platform-tag tag-twitter">Twitter</div>
    <div class="post-text">{content['twitter']}</div>
</div>

<div class="card">
    <div class="section-label">Platform Adapted</div>

    <div class="platform-tag tag-linkedin">LinkedIn</div>
    <div class="post-text">{adapted['linkedin']}</div>

    <div class="divider"></div>

    <div class="platform-tag tag-instagram">Instagram</div>
    <div class="post-text">{adapted['instagram']}</div>

    <div class="divider"></div>

    <div class="platform-tag tag-twitter">Twitter</div>
    <div class="post-text">{adapted['twitter']}</div>
</div>
 
    <!-- Variations Card -->
    <div class="card">
        <div class="section-label">Post Variations</div>
        <ul class="variation-list">
            {''.join(f"<li>{v}</li>" for v in variations)}
        </ul>
    </div>
 
    <a href="/" class="btn-home">← Generate New Strategy</a>
 
</div>

<div class="card">
    <div class="section-label">Publish</div>

    <a href="{links['linkedin_url']}" target="_blank" class="btn-home">
        🚀 Publish on LinkedIn
    </a>

    <a href="{links['twitter_url']}" target="_blank" class="btn-home">
        🐦 Publish on Twitter
    </a>

    <button class="btn-home" onclick="copyInstagram()">
        📸 Copy for Instagram
    </button>
</div>

<script>
function copyInstagram() {
    navigator.clipboard.writeText(`{content['instagram']}`);
    alert("Instagram caption copied! Paste it in app.");
}
</script>
 
</body>
</html>
 
    """


# 🧠 Memory Page
@app.get("/memory", response_class=HTMLResponse)
def view_memory():
    memory = get_memory()

    items = ""
    for item in memory:
        if isinstance(item, dict) and "goal" in item:
            items += f"<li>{item['goal']}</li>"
        else:
            items += f"<li>{str(item)}</li>"

    return f"""
    <h1>Past Strategies</h1>
    <ul>
        {items}
    </ul>
    <a href="/">Back</a>
    """