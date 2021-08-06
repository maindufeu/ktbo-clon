import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
from datetime import date
import subprocess

today = date.today()
print(today)

d2 = timedelta(days = 105)
startDate = str(today-d2)
startDate = f'{startDate}'
print('startdate:',startDate)

ENDPOINT="database-1.cbrebg97dmdd.us-east-2.rds.amazonaws.com"
PORT="3306"
USR="admin"
REGION="us-east-2"
DBNAME="database-1"
PWD = 'Schopenhauer2021*'
DB = 'KTBOKUBEcampaigns'

#now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

#session = boto3.Session(profile_name='default')
#client = session.client('rds')
#token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)

connection_string = f'mysql+pymysql://{USR}:{PWD}@{ENDPOINT}:{PORT}/{DB}'
db = create_engine(connection_string)

df = pd.read_csv('Campaigns/stagging.csv')
df['created_at'] = datetime.now()
df['daily'] = pd.to_datetime(df['daily']).dt.date

try:
    db = create_engine(connection_string)

    get_view = f'SELECT * from kwindaily2 where daily > {startDate}'
    print(get_view)
    result = db.engine.execute(get_view).fetchall()
    df = pd.DataFrame(result)
    df.to_csv('KWIN/kwin90.csv', header=['Campaign Name', 'Campaign Label','Platform','Initiative','Brand','Platform Cost', 'Impressions', 'Clicks', 'Engagements', 'Video Views', 'Video Completions', 'Daily', 'Datasource'], index = False)

except Exception as e:
    print("Database connection failed due to {}".format(e))
