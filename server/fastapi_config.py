from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from logic import reward

app = FastAPI(debug=True)


@app.get("/has-rewards")
async def root(character_name: str):
  result = reward.check_rewards(character_name)
  
  return {
    "has_rewards_available": True if result[0] > 0 else False,
    "count": result[0]
  }


@app.get("/rewards")
async def root(character_name: str):
  result = reward.get_and_consume_rewards(character_name)
  
  return [
    {
      "time_played": tupla[0], 
      "souls_stone": False if(tupla[1] == 0) else True,
      "money": False if(tupla[1] == 0) else True
    } for tupla in result
  ]


def initFastApi():
  origins = ["*"]

  app.add_middleware(
      CORSMiddleware,
      allow_origins=origins,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  
  uvicorn.run(app, host="localhost", port=8000)

