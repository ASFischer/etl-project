from db import DB
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

db = DB(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=int(os.getenv('POSTGRES_PORT', 5432)),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
)

for file in os.listdir('02-silver-validated'):
    df = pd.read_parquet(f'02-silver-validated/{file}')
    db.create_table(
        file.replace('.parquet', ''),
        df
    )
    db.insert_data(
        file.replace('.parquet', ''),
        df
    )

db.close()
