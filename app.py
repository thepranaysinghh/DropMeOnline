from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from engines.strategy_engine import generate_strategy

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

    return f"""
    <h1>Strategy Generated</h1>
    <p><b>Goal:</b> {result['goal']}</p>
    <p><b>Niche:</b> {result['niche']}</p>
    <p><b>Tone:</b> {result['tone']}</p>
    <p><b>Posting:</b> {result['posting_frequency']}</p>
   
     <a href="/">Back</a>
    """