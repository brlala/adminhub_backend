from fastapi import FastAPI
# from .internal import admin
# from app.server.db.client import connect_to_mongo, close_mongo_connection, get_database
from app.server.routers import items, users, students, login, questions, flows, bot, broadcasts, upload, conversations
from app.server.core.env_variables import local_config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
print(local_config.ALLOWED_HOSTS)
# app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=local_config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_event_handler("startup", connect_to_mongo)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(students.router)
app.include_router(login.router)
app.include_router(questions.router)
app.include_router(questions.router)
app.include_router(flows.router)
app.include_router(bot.router)
app.include_router(broadcasts.router)
app.include_router(upload.router)
app.include_router(conversations.router)
# app.include_router(test.router)
# app.add_event_handler("shutdown", close_mongo_connection)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}