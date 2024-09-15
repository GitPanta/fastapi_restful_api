from fastapi import Depends, FastAPI

from app.core.dependencies import get_query_token, get_token_header
from app.core.db import init_db
from app.db import models, database
from app.routers import authentication, elections, records, rosters, users

init_db()

app = FastAPI()


app.include_router(authentication.router)
app.include_router(elections.router)
app.include_router(records.router)
app.include_router(rosters.router)
app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )