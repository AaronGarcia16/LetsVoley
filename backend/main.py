from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI()

# Permitir CORS para que el frontend pueda hacer peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de prueba inicial
@app.get("/")
def read_root():
    return {"message": "Welcome to Let's Voley backend!"}

# Nueva ruta para crear un partido
@app.post("/crear-partido")
async def crear_partido(
    lugar: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(...),
    nivel: str = Form(...),
    comentario: str = Form(None),
    creador: str = Form(...)
):
    nuevo_partido = {
        "lugar": lugar,
        "fecha": fecha,
        "hora": hora,
        "nivel": nivel,
        "comentario": comentario,
        "creador": creador  # <-- Guardamos el creador
    }

    archivo = Path("partidos.json")
    if archivo.exists():
        partidos = json.loads(archivo.read_text())
    else:
        partidos = []

    partidos.append(nuevo_partido)
    archivo.write_text(json.dumps(partidos, indent=2, ensure_ascii=False))

    return {"mensaje": "Partido creado correctamente"}

@app.get("/listar-partidos")
def listar_partidos():
    archivo = Path("partidos.json")
    if archivo.exists():
        partidos = json.loads(archivo.read_text())
    else:
        partidos = []
    return partidos

from fastapi import HTTPException

@app.delete("/eliminar-partido/{indice}")
def eliminar_partido(indice: int):
    archivo = Path("partidos.json")
    if not archivo.exists():
        raise HTTPException(status_code=404, detail="No hay partidos para eliminar.")
    
    partidos = json.loads(archivo.read_text())

    if indice < 0 or indice >= len(partidos):
        raise HTTPException(status_code=404, detail="Índice de partido inválido.")
    
    partidos.pop(indice)
    archivo.write_text(json.dumps(partidos, indent=2, ensure_ascii=False))
    
    return {"mensaje": "Partido eliminado correctamente"}

