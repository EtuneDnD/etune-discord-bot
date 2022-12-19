import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_204_NO_CONTENT

from main.logic.models.reward import Reward
from main.logic.usecases.update_actor.update_actor import UpdateActor
from main.server.dto.actor_update_dto import ActorUpdateDTO

app = FastAPI(debug=True)


@app.get("/has-rewards")
async def root(character_name: str):
    result = Reward.check_rewards(character_name)

    return {
        "has_rewards_available": True if result[0] > 0 else False,
        "count": result[0]
    }


@app.get("/rewards")
async def root(character_name: str):
    result = Reward.get_and_consume_rewards(character_name)

    return [
        {
            "time_played": tupla[0],
            "souls_stone": False if (tupla[1] == 0) else True,
            "money": False if (tupla[1] == 0) else True
        } for tupla in result
    ]


@app.put("/actor/{character_name}", status_code=HTTP_204_NO_CONTENT)
async def root(character_name: str, actor_update: ActorUpdateDTO):
    UpdateActor(character_name, actor_update).execute()


def init_fastapi():
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="localhost", port=8000)
