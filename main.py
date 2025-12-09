from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Eisenhower classifier")

class TasksIn(BaseModel):
    tasks: List[str]

class TasksOut(BaseModel):
    q1: List[str]  # Do now
    q2: List[str]  # Schedule
    q3: List[str]  # Delegate / automate
    q4: List[str]  # Eliminate / park

def simple_rules(task: str) -> str:
    t = task.lower()
    # Q1: cosas con fuerte deadline cercano
    if "tesis" in t or "entregar" in t or "deadline" in t:
        return "q1"
    # Q1: trabajo/carrera con fecha
    if "aplicar" in t or "apply" in t or "trabajo" in t or "job" in t:
        return "q1"
    # Q2: escribir, leer, aprender
    if "escribir" in t or "write" in t or "leer" in t or "read" in t or "paper" in t:
        return "q2"
    # Q3: limpiar, emails, admin
    if "email" in t or "formatear" in t or "admin" in t or "limpiar" in t:
        return "q3"
    # Q4 por defecto
    return "q4"

@app.post("/classify", response_model=TasksOut)
def classify(tasks_in: TasksIn) -> TasksOut:
    buckets: Dict[str, List[str]] = {"q1": [], "q2": [], "q3": [], "q4": []}
    for task in tasks_in.tasks:
        key = simple_rules(task)
        buckets[key].append(task)
    return TasksOut(**buckets)

@app.get("/health")
def health():
    return {"status": "ok"}
