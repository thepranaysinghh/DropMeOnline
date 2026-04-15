from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from engines.strategy_engine import generate_strategy
from engines.variation_engine import generate_variations
from engines.content_generator import generate_content
from engines.platform_adapter import adapt_platform

from core.memory import save_memory, get_memory

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>DropMeOnline</h1>
    <form action="/generate-strategy" method="post">
        <input type="text" name="goal" placeholder="Enter your goal">
        <button type="submit">Generate</button>
    </form>
    """

@app.post("/generate-strategy", response_class=HTMLResponse)
def generate(goal: str = Form(...)):
    result = generate_strategy(goal)
    save_memory(result)
    content = generate_content(goal)
    adapted = adapt_platform(content)
    variations = generate_variations(goal)

    return f"""
<h1>Strategy Generated</h1>

<p><b>Goal:</b> {result['goal']}</p>
<p><b>Niche:</b> {result['niche']}</p>
<p><b>Tone:</b> {result['tone']}</p>
<p><b>Posting:</b> {result['posting_frequency']}</p>

<h3>Content:</h3>
<p><b>LinkedIn:</b> {content['linkedin']}</p>
<p><b>Instagram:</b> {content['instagram']}</p>
<p><b>Twitter:</b> {content['twitter']}</p>

<h3>Platform Adapted:</h3>
<p><b>LinkedIn:</b> {adapted['linkedin']}</p>
<p><b>Instagram:</b> {adapted['instagram']}</p>
<p><b>Twitter:</b> {adapted['twitter']}</p>

<h3>Variations:</h3>
<ul>
    {''.join(f"<li>{v}</li>" for v in variations)}
</ul>

<a href="/">Back</a>
"""
# app.py — Main entry point for DropMeOnline
 
# Initialize FastAPI app
app = FastAPI()
 
# Point to templates folder
templates = Jinja2Templates(directory="templates")
 
# Root endpoint — serves index.html
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
# Memory endpoint — shows past goals as HTML
@app.get("/memory", response_class=HTMLResponse)
def view_memory():
    memory = get_memory()
 
    # Build list items from past goals
    items = "".join(
        f"<li>{entry.get('goal', 'No goal')}</li>"
        for entry in memory
    ) or "<li>No memory yet.</li>"
 
    html = f"""
    <html>
    <head>
        <title>Memory — DropMeOnline</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 60px auto; padding: 0 20px; }}
            h1 {{ font-size: 22px; }}
            li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        </style>
    </head>
    <body>
        <h1>Past Goals</h1>
        <ul>{items}</ul>
        <br><a href="/">← Back</a>
    </body>
    </html>
    """
    return html
 