import os
from fastapi import FastAPI, File, UploadFile
import base64
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import spotipy

load_dotenv()

app = FastAPI()
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

## Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def encode_image64(image):
    readImg = await image.read()
    return base64.b64encode(readImg).decode("utf-8")

with open('./prompts/imagePrompt.txt', 'r') as file:
    fileLines = file.readlines()
    imageToWordsPrompt = " ".join(line.strip() for line in fileLines)      

@app.post('/image')
async def image(file_upload: UploadFile = File(...)):
    
    ## STEP 1: Decode the image, and get its description.
    
    #Use base64 encoding for image
    base64img = await encode_image64(file_upload)
    
    res = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{  
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": imageToWordsPrompt
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64img}"}
                }
            ]
        }]
    )
    
    ## STEP 2: 
    
    return {'message': res.choices[0]}

@app.get('/')
async def mainapi():
    return {'message': 'API Works.3'}
