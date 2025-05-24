from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ativar templates HTML
templates = Jinja2Templates(directory="templates")

# Servir arquivos JSON externos (plugin)
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

@app.get("/")
def home():
    return {"mensagem": "API do Bastos Run Coach está no ar!"}

@app.get("/analisar", response_class=HTMLResponse)
def form_analisar(request: Request):
    return templates.TemplateResponse("analisar.html", {"request": request})

@app.get("/sincronizar")
def sincronizar(periodo: str = "ultimo"):
    return RedirectResponse(url="https://www.strava.com/oauth/authorize")

@app.get("/ultimotreino")
def get_ultimo_treino():
    return {
        "atividade": {
            "distancia": 10.2,
            "tempo": "53:14",
            "elevacao": 120,
            "ritmo_medio": "5:13",
            "frequencia": 152
        }
    }

class Treino(BaseModel):
    distancia: float
    ritmo: str

@app.post("/analisar")
def analisar_treino(dados: Treino):
    return {
        "analise": f"Atividade com {dados.distancia} km a {dados.ritmo}/km foi registrada e será analisada."
    }
