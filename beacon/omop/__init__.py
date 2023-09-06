import psycopg2
from beacon import conf # Maybe we can add the postgresURL in the conf.py file
import os

db_url = os.getenv('POSTGRES_URL', default="postgresql://pgadmin:admin@localhost:5432/omopdb")
client = psycopg2.connect(db_url)