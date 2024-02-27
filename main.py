from uuid import uuid4, UUID
import json
from typing import List, Optional, Union
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


def get_new_uuid() -> str:
    return str(uuid4())


class User(BaseModel):
    id: str = Field(default_factory=get_new_uuid)
    username: str
    email: str
    password: str
    dm: bool = False
    player: bool = True
    lfg: bool = True
    language: list = []
    timestamp: Union[str, None] = None
    games: list = []
    platforms: list = []


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    dm: bool
    player: bool
    lfg: bool
    language: list
    timestamp: str
    games: list
    platforms: list


class Game(BaseModel):
    id: str = Field(default_factory=get_new_uuid)
    name: str


class Platform(BaseModel):
    id: str = Field(default_factory=get_new_uuid)
    name: str
    url: str


app = FastAPI()

USER_JSON = "./database/user.json"
GAME_JSON = "./database/game.json"
PLATFORM_JSON = "./database/platform.json"


@app.get("/users", response_model=List[UserOut])
def get_users_list(skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[UserOut]:
    users = read_json(USER_JSON)

    return users[skip:limit]


@app.get("/user/{user_id}", response_model=UserOut)
def get_user_info(user_id: UUID) -> Union[User, bool]:
    users = read_json(USER_JSON)
    found_user = next((user for user in users if user["id"] == str(user_id)), False)

    if not found_user:
        raise HTTPException(
            status_code=404, detail=f"User with id:{str(user_id)} not found"
        )

    return found_user


@app.post("/user")
def create_new_user(user: User):
    users = read_json(USER_JSON)
    users.append(user.model_dump())

    write_json(data=users, file=USER_JSON)


@app.delete("/user/{user_id}")
def delete_user(user_id: UUID):
    users = read_json(USER_JSON)
    users.remove(get_user_info(user_id))

    write_json(data=users, file=USER_JSON)


@app.get("/games")
def get_games_list(skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[Game]:
    games = read_json(GAME_JSON)

    return games[skip:limit]


@app.get("/game/{game_id}")
def get_game_info(game_id: UUID) -> Union[Game, bool]:
    games = read_json(GAME_JSON)
    found_game = next((game for game in games if game["id"] == str(game_id)), False)

    if not found_game:
        raise HTTPException(
            status_code=404, detail=f"Game with id:{str(game_id)} not found"
        )

    return found_game


@app.post("/game")
def create_game(game: Game):
    games = read_json(GAME_JSON)
    games.append(game.model_dump())

    write_json(data=games, file=GAME_JSON)


@app.delete("/game/{game_id}")
def delete_game(game_id: UUID):
    games = read_json(GAME_JSON)
    games.remove(get_game_info(game_id))

    write_json(data=games, file=GAME_JSON)


@app.get("/platforms")
def get_platforms_list(
    skip: Optional[int] = 0, limit: Optional[int] = 10
) -> List[Platform]:
    platforms = read_json(PLATFORM_JSON)

    return platforms[skip:limit]


@app.get("/platform/{platform_id}")
def get_platform_info(platform_id: UUID) -> Union[Platform, bool]:
    platforms = read_json(PLATFORM_JSON)
    found_platform = next(
        (platform for platform in platforms if platform["id"] == str(platform_id)),
        False,
    )

    if not found_platform:
        raise HTTPException(
            status_code=404, detail=f"Platform with id:{str(platform_id)} not found"
        )

    return found_platform


@app.post("/platform")
def create_platform(platform: Platform):
    platforms = read_json(PLATFORM_JSON)
    platforms.append(platform.model_dump())

    write_json(data=platforms, file=PLATFORM_JSON)


@app.delete("/platform/{platform_id}")
def delete_platform(platform_id: UUID):
    platforms = read_json(PLATFORM_JSON)
    platforms.remove(get_platform_info(platform_id))

    write_json(data=platforms, file=PLATFORM_JSON)


def read_json(file: str) -> list:
    f = open(file)
    data = json.load(f)

    return data


def write_json(data: list, file: str):
    # Serializing json
    json_object = json.dumps(data, indent=4)

    with open(file, "w") as outfile:
        outfile.write(json_object)
