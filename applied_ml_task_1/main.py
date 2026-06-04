from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rag import query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"))
app.mount("/data", StaticFiles(directory="data"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get('/')
def root():
  return FileResponse('frontend/index.html')

@app.get('/query')
def querypage(query_content: str):
  response = query(query_content)
  return {'data': response}


if __name__ == '__main__':
  uvicorn.run(app)