from fastapi import FastAPI

app = FastAPI()

@app.get('/image')
async def image():
    return 'Image endpoint works.'