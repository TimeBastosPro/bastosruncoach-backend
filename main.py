from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"mensagem": "API do Bastos Run Coach está no ar!"}

@app.get("/analisar", response_class=HTMLResponse)
def form_analisar(request: Request):
    return templates.TemplateResponse("analisar.html", {"request": request})
