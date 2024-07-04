from fastapi import FastAPI
from app import routes  # Importe suas rotas ou APIRouter personalizados

app = FastAPI()

# Inclua as rotas do arquivo routes.py
app.include_router(routes.router)  # Supondo que você tenha definido um APIRouter em routes.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)