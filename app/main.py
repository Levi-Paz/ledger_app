import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api import routes
from fastapi.staticfiles import StaticFiles
import os
# from scalar_fastapi import get_scalar_api_reference

description = """
API de Mini-Contabilidade com Transações Atômicas.  
Abaixo é possível encontrar recursos adicionais relacionados à API:

* [Fluxograma API](./static/fluxograma-ledger-api.svg)
* Para acessar a documentação em markdown do fluxograma verifique o repositório no GitHub: [Ledger API Docs](https://github.com/Levi-Paz/ledger_app/docs/fluxograma-ledger-api-md)
""" 

app = FastAPI(
    title="Ledger API",
    description=description,
    version="1.0.0",
    terms_of_service="https://notepad.ink/teste123123",
    contact={
        "name": "Levi Wesley Paz",
    },
    license_info={
        "name": "Isso deveria ser uma licença MIT ou similar",
        "url": "https://notepad.ink/teste123123",
    },
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

app.include_router(routes.router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Ledger API tá online!\nAcesse /docs para ver a documentação."}


@app.get("/scalar", include_in_schema=False)
async def get_scalar_html():
    scalar_options = {
       "theme": "kepler",
       "layout": "modern",
       "darkMode": True,
       "showSidebar": True,
       "searchHotKey": "k",
       "defaultHttpClient": {
          "targetKey": "python",
          "clientKey": "requests"
          }
          }
    config_json = json.dumps(scalar_options)
    html_content = f"""
    <!doctype html>
    <html>
      <head>
        <title>Ledger App - Documentação</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          body {{ margin: 0; }}
        </style>
      </head>
      <body>
        <script
          id="api-reference"
          data-url="/openapi.json" 
          data-proxy-url="https://proxy.scalar.com"
          data-configuration='{config_json}'
        ></script>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)
