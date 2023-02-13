import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_204_NO_CONTENT

from main.db.db_config import connect
from main.logic.usecases.legacy.consume_rewards import ConsumeRewardsUseCase
from main.logic.usecases.legacy.update_actor.update_actor import UpdateActor
from main.server.dto.actor_update_dto import ActorUpdateDTO

app = FastAPI(debug=True)


@app.get("/rewards")
async def root(character_name: str):
    return ConsumeRewardsUseCase(character_name).execute(connect())


@app.put("/actor/{character_name}", status_code=HTTP_204_NO_CONTENT)
async def root(character_name: str, actor_update: ActorUpdateDTO):
    UpdateActor(character_name, actor_update).execute(connect())


def init_fastapi():
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
