from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from engines.strategy_engine import generate_strategy
from engines.variation_engine import generate_variations
from engines.content_generator import generate_content
from engines.platform_adapter import adapt_platform

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
