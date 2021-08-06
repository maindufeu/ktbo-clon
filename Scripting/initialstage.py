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
    df.to_sql(con=db, name='staging', if_exists='replace')
    query = '''SELECT * from staging limit 1'''
    result = db.engine.execute(query).fetchall()
    pr = pd.DataFrame(result)
    print(pr)

    factual_insert = ''' insert into factual_item
    SELECT platform_id, clicks, video_views, video100, engagements, impressions, platform_cost, daily, created_at FROM staging as STG;'''
    result = db.engine.execute(factual_insert)
    query = '''SELECT * from factual_item limit 10'''
    result = db.engine.execute(query).fetchall()
    pr = pd.DataFrame(result)
    print('factual',pr)

    dimension_insert = ''' insert into dimension
	select campaign_name, campaign_label, platform, brand, initiative, platform_id, datasource from staging
    group by campaign_name'''
    result = db.engine.execute(dimension_insert)
    query = '''SELECT * from dimension limit 10'''
    result = db.engine.execute(query).fetchall()
    pr = pd.DataFrame(result)
    print('dimensional',pr)

    get_view = f'SELECT * from kwindaily where daily > {startDate}'
    print(get_view)
    result = db.engine.execute(get_view).fetchall()
    df = pd.DataFrame(result)
    df.to_csv('KWIN/kwin90.csv', header=['campaign_name', 'platform_cost', 'impressions', 'clicks', 'engagements', 'video_views', 'video100', 'daily', 'datasource'], index = False)

except Exception as e:
    print("Database connection failed due to {}".format(e))
