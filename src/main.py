from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from src.tasks.router import router as tasks_router
from src.projects.router import router as projects_router
from src.users.router import router as users_router
from src.categories.router import router as category_router
from src.substacles.router import router as substacles_router
from src.images.router import router as images_router


app = FastAPI()
PORT = 8080
app.mount("/user_image", StaticFiles(directory="user_image"), name="user_image")
app.mount("/project_image", StaticFiles(directory="project_image"), name="project_image")

app.include_router(category_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(substacles_router)
app.include_router(users_router)
app.include_router(images_router)

if __name__ == "__main__":
    uvicorn.run('src.main:app', host='127.0.0.1', port=PORT, reload=True)