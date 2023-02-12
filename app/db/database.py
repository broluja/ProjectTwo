from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings as sttg

MYSQL_URL = f"{sttg.DB_HOST}://{sttg.DB_USER}:{sttg.DB_PASSWORD}@{sttg.DB_HOSTNAME}:{sttg.DB_PORT}/{sttg.DB_NAME}"

engine = create_engine(MYSQL_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# sql_query = """
#     SELECT * FROM fletnix.actors
#     WHERE 1 = 1
#       AND country IN %(categories)s
# """
#
# params = {"categories": ("USA", "Italy")}
#
# with engine.connect() as conn:
#     result = conn.exec_driver_sql(sql_query, params)
#     for row in result:
#         print(row)
