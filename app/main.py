import os

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

DATABASE_URL = os.environ.get("DATABASE_URL", "")

app = FastAPI(title="infra-lab notes API")


class NoteIn(BaseModel):
    text: str


def query(sql, params=()):
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, text TEXT NOT NULL)"
        )
        cur = conn.execute(sql, params)
        return cur.fetchall() if cur.description else []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    try:
        query("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "db unavailable"})


@app.post("/notes", status_code=201)
def add_note(note: NoteIn):
    row = query("INSERT INTO notes (text) VALUES (%s) RETURNING id", (note.text,))
    return {"id": row[0][0], "text": note.text}


@app.get("/notes")
def list_notes():
    rows = query("SELECT id, text FROM notes ORDER BY id")
    return [{"id": r[0], "text": r[1]} for r in rows]
