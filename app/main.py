import uvicorn
from fastapi import FastAPI

from app.db.database import engine, Base
from app.users.routes import user_router, subuser_router, admin_router


Base.metadata.create_all(bind=engine)


def init_app():
    my_app = FastAPI()
    my_app.include_router(user_router)
    my_app.include_router(subuser_router)
    my_app.include_router(admin_router)
    return my_app


app = init_app()


@app.get("/", include_in_schema=False)
def root():
    return {"Hello": "planet Earth!"}


if __name__ == "__main__":
    uvicorn.run(app)
