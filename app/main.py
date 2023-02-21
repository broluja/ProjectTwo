"""Main module"""
import uvicorn
from fastapi import FastAPI

from app.db.database import engine, Base
from app.users.routes import user_router, subuser_router, admin_router
from app.directors.routes import director_router
from app.genres.routes import genre_router
from app.actors.routes import actor_router
from app.movies.routes import movie_router, movie_actor_router, watch_movie
from app.series.routes import series_router, episode_router, series_actor_router, watch_episode


Base.metadata.create_all(bind=engine)


def init_app():
    """
    Initializing app
    :return: None.
    """
    my_app = FastAPI()
    my_app.include_router(user_router)
    my_app.include_router(subuser_router)
    my_app.include_router(admin_router)
    my_app.include_router(watch_movie)
    my_app.include_router(watch_episode)

    my_app.include_router(movie_router)

    my_app.include_router(series_router)
    my_app.include_router(episode_router)

    my_app.include_router(movie_actor_router)
    my_app.include_router(series_actor_router)

    my_app.include_router(actor_router)
    my_app.include_router(director_router)
    my_app.include_router(genre_router)

    return my_app


app = init_app()


@app.get("/", include_in_schema=False)
def root():
    return {"Hello": "planet Earth!"}


if __name__ == "__main__":
    uvicorn.run(app)
