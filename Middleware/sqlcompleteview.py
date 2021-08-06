import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
from datetime import date
import subprocess

today = date.today()
print(today)

ENDPOINT="database-1.cbrebg97dmdd.us-east-2.rds.amazonaws.com"
PORT="3306"
USR="admin"
REGION="us-east-2"
DBNAME="database-1"
PWD = 'Schopenhauer2021*'
DB = 'KTBOKUBEcampaigns'

connection_string = f'mysql+pymysql://{USR}:{PWD}@{ENDPOINT}:{PORT}/{DB}'
db = create_engine(connection_string)

df = pd.read_csv('Campaigns/stagging.csv')
df['created_at'] = datetime.now()
df['daily'] = pd.to_datetime(df['daily']).dt.date

try:
    db = create_engine(connection_string)

    get_view = f'SELECT * from kwindaily2'
    print(get_view)
    result = db.engine.execute(get_view).fetchall()
    df = pd.DataFrame(result)
    df.to_csv('KWIN/kwincomplete.csv', header=['Campaign Name', 'Campaign Label','Platform','Initiative','Brand','Platform Cost', 'Impressions', 'Clicks', 'Engagements', 'Video Views', 'Video Completions', 'Daily', 'Datasource'], index = False)

except Exception as e:
    print("Database connection failed due to {}".format(e))
