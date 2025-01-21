# Import necessary moduls
import pandas as pd
from sqlalchemy import create_engine
from decouple import config


# Load data from csv
data = pd.read_csv('./Data Files/all_seasons.csv')

if data.empty:
    print("The CSV file is empty. Please check the file.")
else:
    print(f"Data loaded successfully.")



# PostgreSQL connection and data upload to SQL database
db_url = config('DB_URL')

try:

    engine = create_engine(db_url)

    data.to_sql('nba_dataset',engine,index=False,if_exists='replace')
    print("Dataset successfully uploaded to SQL Database")

except Exception as e:
    print("An error occured:",e)




