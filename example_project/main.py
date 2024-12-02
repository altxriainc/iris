from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from altxria.iris.engine import TemplateEngine

# Initialize the app and template engine
app = FastAPI()
template_engine = TemplateEngine(template_dir="./templates", cache_enabled=False)

# Home Page
@app.get("/", response_class=HTMLResponse)
def home():
    context = {"user": "Alice"}
    rendered_page = template_engine.render("index.html", context)
    return HTMLResponse(content=rendered_page)

# About Page
@app.get("/about", response_class=HTMLResponse)
def about():
    rendered_page = template_engine.render("about.html", {})
    return HTMLResponse(content=rendered_page)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
