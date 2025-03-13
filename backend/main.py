import os
from fastapi import FastAPI, File, UploadFile
import base64
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from spotipy import Spotify, SpotifyOAuth

load_dotenv()

app = FastAPI()
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
sp = Spotify(auth_manager = SpotifyOAuth(
    client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
))

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
    print("This should print.")
    ## STEP 1: Decode the image, and get its description.
    
    #Use base64 encoding for image
    base64img = await encode_image64(file_upload)
    
    res = openai.chat.completions.create(
        model="gpt-4o",
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
    
    ## STEP 2: Tokenize response from gpt-4o, or detect error.
    
    #gptResponse = res.choices[0]#[0]['message']['content']
    print(res)

    # if gptResponse == "ERRNOPEOPLE":
    #     print("ERRNOPEOPLE Detected.")
    #     return {'message': "Sorry! We can't process images with people in it."}
    
    # musicInfo = gptResponse.split('/')
    # print("MUSIC INFO = ", musicInfo)
    
    ## STEP 3: Use Spotify API to find music. (GENRE/TEMPO/DANCEABILITY/ENERGY/VALENCE/ACOUSTICNESS/INSTRUMENTALNESS)

    #KEEP IN MIND: You should get the music info as a JSON object earlier for easier mapping here.
    # recommendations = sp.recommendations(
    #     seed_genres=[musicInfo[0]],
    #     limit=1,
    #     target_tempo=float(musicInfo[1]),
    #     target_danceability=float(musicInfo[2]),
    #     target_energy=float(musicInfo[3]),
    #     target_valence=float(musicInfo[4]),
    #     target_acousticness=float(musicInfo[5]),
    #     target_instrumentalness=float(musicInfo[6]),
    # )
    
    # track = recommendations
    # print(track)
    #outputSong = f"{track['name']} by {track['artists'][0]['name']}"
    return {'message': res.choices[0]}

@app.get('/')
async def mainapi():
    return {'message': 'API Works.'}
