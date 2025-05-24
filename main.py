from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensagem": "API do Bastos Run Coach está no ar!"}

@app.get("/ultimotreino")
def ultimo_treino():
    return {"distancia_km": 10.5, "ritmo": "5:15", "frequencia_cardiaca": 145}

@app.post("/analisar")
def analisar_treino(atividade: dict):
    return {
        "analise": f"O treino de {atividade['distancia']} km foi bem executado. Ritmo: {atividade['ritmo']} min/km."
    }

@app.get("/sincronizar")
def sincronizar():
    return {"mensagem": "Redirecionar para login no Strava"}

@app.get("/analisar", response_class=HTMLResponse)
def form_analisar(request: Request):
    return templates.TemplateResponse("analisar.html", {"request": request})
