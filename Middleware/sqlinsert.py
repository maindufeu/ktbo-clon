import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
from datetime import date
import subprocess

today = date.today()
d2 = timedelta(days = 105)
startDate = str(today-d2)
startDate = f'{startDate}'
print('startdate:',startDate)
df = pd.read_csv('Campaigns/stagging.csv')
df['created_at'] = datetime.now()
df['daily'] = pd.to_datetime(df['daily']).dt.date

ENDPOINT="database-1.cbrebg97dmdd.us-east-2.rds.amazonaws.com"
PORT="3306"
USR="admin"
REGION="us-east-2"
DBNAME="database-1"
PWD = 'Schopenhauer2021*'
DB = 'KTBOKUBEcampaigns'

connection_string = f'mysql+pymysql://{USR}:{PWD}@{ENDPOINT}:{PORT}/{DB}'
db = create_engine(connection_string)

try:
    db = create_engine(connection_string)
    df.to_sql(con=db, name='staging', if_exists='replace')
    query = '''SELECT * from staging limit 1'''
    result = db.engine.execute(query).fetchall()
    pr = pd.DataFrame(result)
    print(pr)

    duplicates_tt = ''' create TABLE duplicates
	select STG.platform_id as duplicated_id from staging as STG
    JOIN factual_item as TGT on STG.platform_id = TGT.platform_id and STG.daily = TGT.daily'''
    result = db.engine.execute(duplicates_tt)

    factual_insert = ''' insert into factual_item
    SELECT platform_id, clicks, video_views, video100, engagements, impressions, platform_cost, daily, created_at FROM staging as STG
    where platform_id not in (select duplicated_id from duplicates);'''
    result = db.engine.execute(factual_insert)
    query = '''SELECT * from factual_item limit 10'''
    result = db.engine.execute(query).fetchall()
    pr = pd.DataFrame(result)
    print('factual',pr)

    dimension_insert = ''' insert into dimension
	select campaign_name, campaign_label, platform, brand, initiative, platform_id, datasource from staging
    where platform_id not in (select duplicated_id from duplicates)
    group by campaign_name'''
    result = db.engine.execute(dimension_insert)
    query = '''SELECT * from dimension limit 10'''
    result = db.engine.execute(query).fetchall()
    pr = pd.DataFrame(result)
    print('dimensional',pr)

    drop_duplicates = '''DROP TABLE duplicates;'''
    result = db.engine.execute(drop_duplicates)

    get_view = f'SELECT * from kwindaily2 where daily > {startDate}'
    print(get_view)
    result = db.engine.execute(get_view).fetchall()
    df = pd.DataFrame(result)
    df.to_csv('KWIN/kwin90.csv', header=['Campaign Name', 'Campaign Label','Platform','Initiative','Brand','Platform Cost', 'Impressions', 'Clicks', 'Engagements', 'Video Views', 'Video Completions', 'Daily', 'Datasource'], index = False)

except Exception as e:
    print("Database connection failed due to {}".format(e))

subprocess.call('git add .', shell=True)
subprocess.call('git commit -m "campaigns kwinunified update"', shell=True)
subprocess.call('git push', shell=True)
