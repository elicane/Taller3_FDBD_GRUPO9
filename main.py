from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#os.environ para despliegue. Descomente cuando ya probó todo local.
client = MongoClient(os.environ["MONGO_URL"])
# TODO: conectarse al cluster Admonsis  

# TODO: conectarse a la base de datos Admonsis  
# db = client["ISIS*******"]
db = client["ISIS2304E27202620"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db["comentarios_bares"].find({"bar_id": bar_id},{"_id":0}))
    return comentarios or {}

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.get('/bares/{bar_id}/eventos')
def getEventos(bar_id:int):
    eventos = list(db["eventos"].find({"bar_id":bar_id},{"_id":0}))
    return (eventos or {})

@app.post('/bares/{bar_id}/eventos')
def getEventos(bar_id:int, datos: dict):
    datos["bar_id"] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento creado'}