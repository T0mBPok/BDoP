from fastapi import FastAPI
import uvicorn

from src.tasks.router import router as tasks_router
from src.projects.router import router as projects_router


app = FastAPI()
PORT = 8080

@app.get('/')
def root():
    return {'ok':True}

app.include_router(tasks_router)
app.include_router(projects_router)

if __name__ == "__main__":
    uvicorn.run('src.main:app', host='127.0.0.1', port=PORT, reload=True)