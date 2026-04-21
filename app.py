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
    prompt_data = understand_prompt(goal)
    mind = build_mastermind(goal, prompt_data)
    save_memory(result)

    content = generate_content(goal)
    plan = decide_post_plan(goal)
    growth = decide_growth_strategy(goal, "linkedin", {"engagement": "high", "last_posts": 5})
    brain = analyze_and_decide("linkedin", {
    "reach": 1200,
    "likes": 85,
    "comments": 14,
    "post_time": "09:00",
    "frequency": "daily"
})
    feedback_result = analyze_feedback("linkedin", {
    "reach": "medium",
    "likes": "high",
    "comments": "medium",
    "time": "morning",
    "overall": "good"
})
    adapted = adapt_platform(content)
    links = generate_publish_links(content)
    variations = generate_variations(goal)
    campaign = generate_campaign(goal, 30, prompt_data['platforms'] if prompt_data['platforms'] else ["linkedin"])
    distribution = create_distribution_plan(
    30,
    prompt_data['platforms'] if prompt_data['platforms'] else ["linkedin"],
    2
)
    conversion = generate_conversion_assets(goal)
    visuals = generate_visual_assets(goal, content['linkedin'])
    market = analyze_market(goal)
    publish = build_publish_queue(
    campaign,
    prompt_data['platforms'] if prompt_data['platforms'] else ["linkedin"]
)

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

<!-- Prompt Understanding Card -->
<div class="card">
    <div class="section-label">Prompt Understanding</div>

    <div class="strategy-grid">
        <div class="stat-box">
            <div class="stat-label">Product</div>
            <div class="stat-value">{prompt_data['product']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Audience</div>
            <div class="stat-value">{prompt_data['audience']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Goal</div>
            <div class="stat-value">{prompt_data['goal']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Tone</div>
            <div class="stat-value">{prompt_data['tone']}</div>
        </div>

        <div class="stat-box">
    <div class="stat-label">Platforms</div>
    <div class="stat-value">{', '.join(prompt_data['platforms']) if prompt_data['platforms'] else 'Not specified'}</div>
</div>

<div class="stat-box">
    <div class="stat-label">Suggestions</div>
    <div class="stat-value">{', '.join(prompt_data['suggested_platforms']) if prompt_data['suggested_platforms'] else 'None'}</div>
</div>

    </div>
</div>

<!-- Mastermind Brain Card -->
<div class="card">
    <div class="section-label">Mastermind Brain</div>

    <div class="strategy-grid">
        <div class="stat-box">
            <div class="stat-label">Core Angle</div>
            <div class="stat-value">{mind['core_angle']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Trigger</div>
            <div class="stat-value">{mind['psychology_trigger']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Hook Style</div>
            <div class="stat-value">{mind['hook_style']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Tone</div>
            <div class="stat-value">{mind['tone']}</div>
        </div>
    </div>

    <div class="divider"></div>

    <div class="post-text"><b>Top Hooks:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in mind['top_hooks'][:3])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>CTA Style:</b> {mind['cta_style']}</div>
</div>


<!-- AI Brain Decision Card -->
<div class="card">
    <div class="section-label">AI Brain Decision</div>

    <div class="strategy-grid">
        <div class="stat-box">
            <div class="stat-label">Next Post Time</div>
            <div class="stat-value">{brain['next_post_time']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Frequency</div>
            <div class="stat-value">{brain['frequency_change']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Content Style</div>
            <div class="stat-value">{brain['content_style']}</div>
        </div>
    </div>

    <div class="divider"></div>

    <div class="post-text">{brain['reason']}</div>
</div>

<!-- Feedback Learning Card -->
<div class="card">
    <div class="section-label">Feedback Learning</div>

    <div class="strategy-grid">
        <div class="stat-box">
            <div class="stat-label">Next Time</div>
            <div class="stat-value">{feedback_result['next_time']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Frequency</div>
            <div class="stat-value">{feedback_result['frequency']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Style</div>
            <div class="stat-value">{feedback_result['content_style']}</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Decision</div>
            <div class="stat-value">{feedback_result['decision']}</div>
        </div>
    </div>
</div>

<!-- quick_feedback_form.html — Compact feedback form snippet -->
<!-- Drop inside any page using existing glassmorphism card style -->
 
<div class="card">
 
    <div class="section-label">Update AI Learning</div>
 
    <form action="/feedback" method="post">
 
        <!-- Hidden platform field -->
        <input type="hidden" name="platform" value="linkedin" />
 
        <div class="form-row">
 
            <div class="form-group">
                <label>Reach</label>
                <select name="reach">
                    <option value="high">High</option>
                    <option value="medium" selected>Medium</option>
                    <option value="low">Low</option>
                </select>
            </div>
 
            <div class="form-group">
                <label>Likes</label>
                <select name="likes">
                    <option value="high">High</option>
                    <option value="medium" selected>Medium</option>
                    <option value="low">Low</option>
                </select>
            </div>
 
            <div class="form-group">
                <label>Comments</label>
                <select name="comments">
                    <option value="high">High</option>
                    <option value="medium" selected>Medium</option>
                    <option value="low">Low</option>
                </select>
            </div>
 
            <div class="form-group">
                <label>Overall</label>
                <select name="overall">
                    <option value="good">Good</option>
                    <option value="average" selected>Average</option>
                    <option value="bad">Bad</option>
                </select>
            </div>
 
        </div>
 
        <br>
        <button type="submit" class="btn-home">Update AI Learning →</button>
 
    </form>
 
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

<div class="card">
    <div class="section-label">Publish</div>

    <a href="{links['linkedin_url']}" target="_blank" class="btn-home">
        🚀 Publish on LinkedIn
    </a>

    <a href="{links['twitter_url']}" target="_blank" class="btn-home">
        🐦 Publish on Twitter
    </a>

    <div class="post-text">
        📸 Instagram Caption:<br><br>
        {content['instagram']}
    </div>
</div>

<!-- Campaign Plan Card -->
<div class="card">
    <div class="section-label">30 Day Campaign Plan</div>

    <ul class="variation-list">
        {''.join(
            f"<li><b>Day {item['day']}:</b> {item['theme']} — {item['hook']}</li>"
            for item in campaign[:10]
        )}
    </ul>

    <div class="post-text" style="margin-top:12px;">
        Showing first 10 days preview.
    </div>
</div>

<!-- Distribution Plan Card -->
<div class="card">
    <div class="section-label">Distribution Plan</div>

    <ul class="variation-list">
        {''.join(
            f"<li><b>Day {item['day']}:</b> {item['platform'].title()} Page {item['page']} — {item['post_type']}</li>"
            for item in distribution[:10]
        )}
    </ul>

    <div class="post-text" style="margin-top:12px;">
        Showing first 10 rollout actions.
    </div>
</div>

<!-- Conversion Engine Card -->
<div class="card">
    <div class="section-label">Conversion Assets</div>

    <div class="post-text"><b>CTA:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in conversion['cta'][:3])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Urgency:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in conversion['urgency'][:2])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Trust:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in conversion['trust'][:2])}
    </ul>
</div>

<!-- Visual Assets Card -->
<div class="card">
    <div class="section-label">Visual Production Engine</div>

    <div class="post-text"><b>LinkedIn Carousel:</b> {visuals['linkedin_carousel']['headline']}</div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in visuals['linkedin_carousel']['slides'][:5])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Instagram Creative:</b> {visuals['instagram_post']['headline']}</div>
    <div class="post-text">{visuals['instagram_post']['caption_text']}</div>

    <div class="divider"></div>

    <div class="post-text"><b>Twitter Graphic:</b> {visuals['twitter_graphic']['headline']}</div>

    <div class="divider"></div>

    <div class="post-text"><b>Image Prompts:</b></div>
    <ul class="variation-list">
        <li>LinkedIn: {visuals['image_prompts']['linkedin']}</li>
        <li>Instagram: {visuals['image_prompts']['instagram']}</li>
        <li>Twitter: {visuals['image_prompts']['twitter']}</li>
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Creative Style:</b></div>
    <ul class="variation-list">
        <li>LinkedIn: {visuals['styles']['linkedin']}</li>
        <li>Instagram: {visuals['styles']['instagram']}</li>
        <li>Twitter: {visuals['styles']['twitter']}</li>
    </ul>
</div>

<!-- Competitor Intelligence Card -->
<div class="card">
    <div class="section-label">Competitor Intelligence</div>

    <div class="post-text"><b>Competitors:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in market['competitors'][:3])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Trends:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in market['trends'][:3])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Opportunities:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in market['opportunities'][:3])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Viral Hooks:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in market['viral_hooks'][:3])}
    </ul>
</div>

<!-- Publishing Workflow Card -->
<div class="card">
    <div class="section-label">Publishing Workflow</div>

    <div class="post-text"><b>Today's Ready Posts:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x['platform'].title()} — {x['title']} ({x['status']})</li>" for x in publish['today'][:5])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Upcoming Queue:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>Day {x['day']} — {x['platform'].title()} — {x['title']}</li>" for x in publish['upcoming'][:5])}
    </ul>

    <div class="divider"></div>

    <div class="post-text"><b>Actions:</b></div>
    <ul class="variation-list">
        {''.join(f"<li>{x}</li>" for x in publish['actions'][:5])}
    </ul>
</div>
 
</body>
</html>
 
    """

@app.post("/update-feedback", response_class=HTMLResponse)
def update_feedback(
    reach: str = Form(...),
    likes: str = Form(...),
    comments: str = Form(...),
    overall: str = Form(...),
    platform: str = Form(...)
):
    result = analyze_feedback(platform, {
        "reach": reach,
        "likes": likes,
        "comments": comments,
        "time": "recent",
        "overall": overall
    })

    return f"""
    <html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Learning Updated — DropMeOnline</title>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ margin:0; padding:0; box-sizing:border-box; }}

        body {{
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #1a1a3e 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            overflow-x: hidden;
        }}

        /* Ambient orbs */
        .orb {{ position:fixed; border-radius:50%; filter:blur(90px); pointer-events:none; z-index:0; }}
        .orb-1 {{ width:480px; height:480px; background:#6d28d9; opacity:0.2; top:-120px; left:-120px; }}
        .orb-2 {{ width:380px; height:380px; background:#1d4ed8; opacity:0.18; bottom:-80px; right:-80px; }}

        .wrapper {{
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 580px;
        }}

        /* Back link */
        .back {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: rgba(255,255,255,0.3);
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-decoration: none;
            margin-bottom: 28px;
            transition: color 0.2s;
        }}
        .back:hover {{ color: #a78bfa; }}

        /* Success banner */
        .banner {{
            background: linear-gradient(135deg, rgba(109,40,217,0.3), rgba(37,99,235,0.25));
            border: 1px solid rgba(167,139,250,0.25);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 0 40px rgba(109,40,217,0.15);
        }}

        .banner-icon {{
            font-size: 36px;
            margin-bottom: 12px;
            display: block;
        }}

        .banner-title {{
            font-family: 'Syne', sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.3px;
            margin-bottom: 6px;
        }}

        .banner-sub {{
            font-size: 13px;
            color: rgba(255,255,255,0.4);
        }}

        /* Glass card */
        .card {{
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 24px;
            padding: 32px;
            margin-bottom: 16px;
            box-shadow: 0 24px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.07);
        }}

        .section-label {{
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            color: #7c3aed;
            margin-bottom: 18px;
        }}

        /* Stats grid */
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }}

        .stat {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 14px;
            padding: 16px 18px;
            transition: border-color 0.25s, background 0.25s;
        }}
        .stat:hover {{ border-color: rgba(124,58,237,0.35); background: rgba(124,58,237,0.06); }}

        .stat-full {{ grid-column: span 2; }}

        .stat-label {{
            font-size: 10px;
            font-weight: 600;
            color: rgba(255,255,255,0.28);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
        }}

        .stat-value {{
            font-size: 15px;
            font-weight: 500;
            color: #e2e8f0;
            line-height: 1.4;
        }}

        /* Platform pill */
        .platform-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(37,99,235,0.2);
            border: 1px solid rgba(37,99,235,0.35);
            color: #93c5fd;
            font-size: 13px;
            font-weight: 600;
            padding: 6px 16px;
            border-radius: 20px;
            text-transform: capitalize;
        }}

        /* Decision badge */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }}
        .badge-keep   {{ background: rgba(134,239,172,0.12); border: 1px solid rgba(134,239,172,0.3); color: #86efac; }}
        .badge-change {{ background: rgba(252,165,165,0.12); border: 1px solid rgba(252,165,165,0.3); color: #fca5a5; }}

        /* Style value */
        .style-value {{
            font-size: 14px;
            font-weight: 400;
            color: #c4b5fd;
            line-height: 1.7;
        }}

        /* Divider */
        .divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
            margin: 6px 0 18px;
        }}

        /* Buttons */
        .btn-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 8px;
        }}

        .btn-primary {{
            display: block;
            text-align: center;
            padding: 14px;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            letter-spacing: 0.3px;
            color: #ffffff;
            background: linear-gradient(135deg, #6d28d9, #2563eb);
            border-radius: 12px;
            text-decoration: none;
            box-shadow: 0 6px 24px rgba(109,40,217,0.35);
            transition: opacity 0.2s, transform 0.15s;
        }}
        .btn-primary:hover {{ opacity:0.88; transform:translateY(-2px); }}

        .btn-secondary {{
            display: block;
            text-align: center;
            padding: 14px;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            letter-spacing: 0.3px;
            color: rgba(255,255,255,0.6);
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            text-decoration: none;
            transition: background 0.2s, color 0.2s;
        }}
        .btn-secondary:hover {{ background: rgba(255,255,255,0.09); color: #fff; }}
    </style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<div class="wrapper">

    <a href="/" class="back">← Back to Home</a>

    <!-- Success banner -->
    <div class="banner">
        <span class="banner-icon">🧠</span>
        <div class="banner-title">AI Learning Updated</div>
        <div class="banner-sub">Strategy adjusted based on your feedback</div>
    </div>

    <!-- Result card -->
    <div class="card">
        <div class="section-label">Updated Strategy</div>

        <div class="grid">

            <div class="stat">
                <div class="stat-label">Platform</div>
                <div class="stat-value">
                    <span class="platform-pill">{platform}</span>
                </div>
            </div>

            <div class="stat">
                <div class="stat-label">Decision</div>
                <div class="stat-value">
                    <span class="badge badge-{result['decision']}">{result['decision'].upper()}</span>
                </div>
            </div>

            <div class="stat">
                <div class="stat-label">Next Post Time</div>
                <div class="stat-value">{result['next_time']}</div>
            </div>

            <div class="stat">
                <div class="stat-label">Frequency</div>
                <div class="stat-value">{result['frequency']}</div>
            </div>

            <div class="divider" style="grid-column:span 2; margin:4px 0;"></div>

            <div class="stat stat-full">
                <div class="stat-label">Recommended Style</div>
                <div class="style-value">{result['content_style']}</div>
            </div>

        </div>
    </div>

    <!-- Action buttons -->
    <div class="btn-row">
        <a href="/" class="btn-secondary">← Home</a>
        <a href="/" class="btn-primary">New Strategy →</a>
    </div>

</div>

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