import json

from fastapi import FastAPI, Request

PATH = "notes.json"
app = FastAPI()


def read_notes(path=PATH) -> list[dict[str, str]]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_notes(notes: list[dict[str, str]], path=PATH):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)


@app.get("/")
def read_root():
    return read_notes()


@app.post("/")
async def post_root(r: Request):
    notes = read_notes()
    new_note = await r.json()
    if 'title' not in new_note or 'text'not in new_note:
        return {"Ошибка": "используйте ключи title и text"}
    notes.append(
        {
            "title": new_note['title'],
            "text": new_note['text']
        }
    )
    save_notes(notes)
    return {'Сообщение': "ок!"}
