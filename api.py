from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

from db import CrossingsDB

from models import CrossingPydantic, CrossingInPydantic

app = FastAPI()
db = CrossingsDB(app, "pereval")

BAD_REQUEST_RESPONSE = JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Invalid fields", "status": 400}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return BAD_REQUEST_RESPONSE

@app.get("/submitData/{item_id}", response_model=CrossingPydantic)
async def get_crossing(item_id: int):
    crossing = await db.get_crossing(item_id)
    print(crossing.__dict__)
    return  CrossingPydantic.from_tortoise_orm(crossing) if crossing else {}


@app.post("/submitData")
async def update_crossing(crossing: CrossingInPydantic):
    d = crossing.dict(exclude_unset=True)
    if crossing := await db.try_to_add_crossing(d):
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Success", "status": 200,
                                     "id": crossing.id})
    return BAD_REQUEST_RESPONSE
