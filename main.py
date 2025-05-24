from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import httpx

app = FastAPI()

# Pastas para arquivos estáticos e templates
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")
templates = Jinja2Templates(directory="templates")

# Página HTML para selecionar análise
@app.get("/analisar", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("analisar.html", {"request": request})

# Endpoint para servir o openapi.yaml
@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    return FileResponse("openapi.yaml", media_type="text/yaml")

# Sincronização com Strava (login)
@app.get("/sincronizar")
async def sincronizar():
    client_id = os.getenv("CLIENT_ID")
    redirect_uri = os.getenv("REDIRECT_URI")
    url = (
        f"https://www.strava.com/oauth/authorize?client_id={client_id}"
        f"&response_type=code&redirect_uri={redirect_uri}"
        f"&approval_prompt=force&scope=activity:read"
    )
    return RedirectResponse(url)

# Callback do Strava (após autorização)
@app.get("/callback")
async def callback(code: str):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    async with httpx.AsyncClient() as client:
        token_response = await client.post("https://www.strava.com/oauth/token", data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code"
        })

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return {"erro": "Token inválido ou expirado"}

        # Buscar última atividade
        activities_response = await client.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        atividades = activities_response.json()
        if not atividades:
            return {"erro": "Nenhuma atividade encontrada"}

        return {"atividade": atividades[0]}

# API externa para o GPT → Analisar uma atividade
@app.post("/analisar")
async def analisar(distancia: float = Form(...), ritmo: str = Form(...)):
    return {
        "analise": (
            f"Com base na distância de {distancia:.2f} km e ritmo de {ritmo}, "
            "o atleta demonstra consistência e bom controle de intensidade. "
            "Recomenda-se intercalar treinos leves e moderados com estímulos de velocidade."
        )
    }

# API externa para o GPT → Retorna último treino (exemplo estático)
@app.get("/ultimotreino")
async def ultimotreino():
    return {
        "atividade": {
            "distancia_km": 7.2,
            "ritmo_medio": "5:30/km",
            "tempo_total": "00:39:45",
            "elevacao": "435m"
        }
    }
