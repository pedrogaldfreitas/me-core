from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
API_KEY = open("API_KEY", "r").read()

## Allow requests from frontend:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/image')
async def image():
    return {'message': 'Image endpoint works.'}