from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'



#  engine resonsible for establishing conneciton with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, 
                            bind=engine)

Base = declarative_base()

# Dependancy for SQLALCHEMY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# # Code to connect to db
# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='Onozero21.',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succesfull!')
#         break

#     except Exception as error:
#         print('Connecting to db failed')
#         print('Error: ', error)
#         time.sleep(2)