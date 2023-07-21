from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

from db import CrossingsDB

from models import CrossingPydantic, CrossingOptional

from os import getenv

app = FastAPI()
FSTR_DB_NAME = getenv("FSTR_DB_NAME", "pereval")
db = CrossingsDB(app, FSTR_DB_NAME)

BAD_REQUEST_RESPONSE = JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Invalid fields", "status": 400}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return BAD_REQUEST_RESPONSE


@app.get("/submitData/")
async def get_crossing_with_email(user_email: str, response_model=list[CrossingPydantic]):
    crossings = await db.get_crossings_by_email(user_email)
    return await CrossingPydantic.from_queryset(crossings)
@app.get("/submitData/{item_id}", response_model=CrossingPydantic)
async def get_crossing(item_id: int):
    crossing = await db.get_crossing(item_id)
    if crossing is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Crossing doesn`t exists"})
    return await CrossingPydantic.from_tortoise_orm(crossing)

@app.patch("/submitData/{item_id}")
async def patch_crossing(item_id: int, crossing: CrossingOptional):
    if await db.try_to_update_crossing_data(item_id, crossing.dict(exclude_unset=True)):
        return JSONResponse(status_code=status.HTTP_200_OK, content={"state": 1})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"state": 0, "message": "Неудача"})

@app.post("/submitData", response_model=CrossingPydantic)
async def update_crossing(crossing: CrossingPydantic):
    d = crossing.dict(exclude_unset=True)
    if crossing := await db.try_to_add_crossing(d):
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Success", "status": 200,
                                     "id": crossing.id})
    return BAD_REQUEST_RESPONSE
